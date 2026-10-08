import { Space, Tag, Tooltip, Typography } from 'antd'

const { Text } = Typography

interface TraceIdPanelProps {
  traceId: string | null | undefined
  traceUrl?: string | null
}

/** 单行 trace 信息条：截断显示 trace_id + 复制按钮 + 可选 LangSmith 跳转链 */
export function TraceIdPanel({ traceId, traceUrl }: TraceIdPanelProps) {
    // 如果没有 traceId（比如没开启 LangSmith），这个组件就什么都不显示（返回 null）
    if (!traceId) return null

    // 如果 ID 超过 8 位，就只切前 8 位，后面加 ... 看起来清爽
  const short = traceId.length > 8 ? `${traceId.slice(0, 8)}...` : traceId

  return (
    <div
      style={{
        marginTop: 12,
        padding: '6px 10px',
        background: '#fafafa',
        borderRadius: 6,
        fontSize: 12,
      }}
    >
        <Space size={8} wrap>
        <Tag color="default" style={{ marginInlineEnd: 0 }}>
          Trace
        </Tag>
        {/* 鼠标悬停时显示完整 ID */}
        <Tooltip title={traceId}>
          <Text
            type="secondary"
            copyable={{ text: traceId, tooltips: ['复制 trace_id', '已复制'] }}
            style={{ fontFamily: 'monospace' }}
          >
            {short}
          </Text>
          </Tooltip>
          {/* 如果有 URL，才渲染链接；没有就不渲染 */}
          {traceUrl ? (
          <a href={traceUrl} target="_blank" rel="noreferrer">
            在 LangSmith 中查看 ↗
          </a>
        ) : null}
        </Space>
    </div>
  )
}