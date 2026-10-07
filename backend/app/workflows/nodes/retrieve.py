"""retrieve: 混合检索，只负责召回 Top-K 候选。

拒答逻辑已搬到 refuse 节点；判定逻辑搬到 judge_context 节点；
本节点现在只负责"召回尽量多的候选"，交给下游 rerank 精排。
"""
from app.core.config import settings
from app.retrieval.vector_retriever import RetrievedChunk
from app.workflows.rag_state import RAGState
from app.retrieval.hybrid_retriever import HybridRetriever

async def retrieve(state: RAGState) -> RAGState:
    retriever = HybridRetriever()
    recall_top_k = settings.retrieval_recall_top_k

    if state.get("route") == "multi_query" and state.get("multi_queries"):
        # 各子查询独立走 hybrid 检索，再合并；不做嵌套 RRF
        bundles: list[list[RetrievedChunk]] = []
        for sub_query in state["multi_queries"] or []:
            bundles.append(
                await retriever.search(
                    sub_query,
                    recall_top_k=recall_top_k,
                    final_top_k=recall_top_k,
                )
            )
        chunks = _merge_chunks(bundles, top_k=recall_top_k,)
    else:
        chunks = await retriever.search(
            state["query"],
            recall_top_k=recall_top_k,
            final_top_k=recall_top_k,
        )
    
    return {"retrieved_chunks": chunks}



def _merge_chunks(
    bundles: list[list[RetrievedChunk]], top_k: int
) -> list[RetrievedChunk]:
    """多路召回结果去重 + 取 Top-K。

    同一个 chunk 可能在多条子查询中都命中；保留 RRF 分最高的那条，
    再整体按 RRF 分降序取前 top_k
    """
    best: dict[str, RetrievedChunk] = {}
    for bundle in bundles:
        for chunk in bundle:
            key = str(chunk.chunk_id)
            prev = best.get(key)
            if prev is None or (chunk.rrf_score or 0.0) > (prev.rrf_score or 0.0):
                best[key] = chunk
    ranked = sorted(best.values(), key=lambda c: c.rrf_score or 0.0, reverse=True)
    return ranked[:top_k]