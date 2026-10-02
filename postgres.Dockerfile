# ===== 阶段 1：构建阶段 =====
FROM postgres:16-bookworm AS builder

ARG PG_MAJOR=16
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        postgresql-server-dev-${PG_MAJOR} \
    && rm -rf /var/lib/apt/lists/*

# 编译安装 SCWS（zhparser 的底层中文分词库）
RUN curl -fsSL http://www.xunsearch.com/scws/down/scws-1.2.3.tar.bz2 -o /tmp/scws.tar.bz2 \
    && mkdir -p /tmp/scws \
    && tar -xjf /tmp/scws.tar.bz2 -C /tmp/scws --strip-components=1 \
    && cd /tmp/scws \
    && ./configure \
    && make -j"$(nproc)" \
    && make install

# 编译安装 zhparser 本体
RUN git clone --depth 1 https://github.com/amutu/zhparser.git /tmp/zhparser \
    && cd /tmp/zhparser \
    && make \
    && make install

# ===== 阶段 2：运行阶段 =====
FROM pgvector/pgvector:pg16

ARG PG_MAJOR=16

# 拷贝编译产物
COPY --from=builder /usr/lib/postgresql/${PG_MAJOR}/lib/zhparser.so /usr/lib/postgresql/${PG_MAJOR}/lib/
COPY --from=builder /usr/local/lib/libscws.* /usr/local/lib/
COPY --from=builder /usr/share/postgresql/${PG_MAJOR}/extension/zhparser* /usr/share/postgresql/${PG_MAJOR}/extension/
COPY --from=builder /usr/share/postgresql/${PG_MAJOR}/tsearch_data/ /usr/share/postgresql/${PG_MAJOR}/tsearch_data/

# 刷新动态链接器缓存，让 PG 启动时能找到 libscws.so
RUN ldconfig