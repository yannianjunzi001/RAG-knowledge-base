"""FastMCP 实例与工具注册入口。

部署模式：
- stateless_http=True: 每次工具调用独立处理，不维护跨请求 session；
  与 RAG 一次性问答语义天然契合，方便横向扩容
- json_response=True: 响应直接 JSON，不走 SSE，降低浏览器 / Agent 客户端集成
- streamable_http_path="/": 让最终挂载路径为 `/mcp` 而非 `/mcp/mcp`（默认行为）
"""

from mcp.server.fastmcp import FastMCP

from app.mcp_server.tools import register_tools

knowledge_mcp = FastMCP(
    name="rag-knowledge-base",
    instructions=(
        "知识库工具集：先调 ask_knowledge_base 直接回答；"
        "调 list_documents / get_document_status / get_knowledge_base_stats 查概览；"
        "管理员可调 upload_document 上传新文件。"
    ),
    stateless_http=True,
    json_response=True,
    streamable_http_path="/",
)

register_tools(knowledge_mcp)