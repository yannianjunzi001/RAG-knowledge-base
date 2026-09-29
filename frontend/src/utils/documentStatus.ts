import type { DocumentRead } from '@/client/types.gen'

// 从生成的类型中提取状态字段的类型
type DocumentStatus = DocumentRead['status']

// 终态集合：用于判断轮询是否应该停止（后续结合 useQuery 的 refetchInterval 使用）
const TERMINAL_STATUSES: ReadonlySet<DocumentStatus> = new Set(['ready', 'failed'])

// 中文状态映射表
const STATUS_LABELS: Record<DocumentStatus, string> = {
    uploading: '上传中',
    parsing: '解析中',
    indexing: '索引中',
    ready: '已就绪',
    failed: '失败',
}

// Ant Design Tag 颜色映射表
const STATUS_COLORS: Record<DocumentStatus, string> = {
    uploading: 'blue',
    parsing: 'cyan',
    indexing: 'geekblue',
    ready: 'green',
    failed: 'red',
}

/**
 * 判断文档是否处于终态。
 * 如果不是终态（即 parsing/uploading/indexing），前端应该继续轮询获取最新状态。
 */
export function isTerminalStatus(status: DocumentStatus): boolean {
    return TERMINAL_STATUSES.has(status)
}

/** 获取状态的中文显示文案 */
export function getStatusLabel(status: DocumentStatus): string {
    return STATUS_LABELS[status]
}

/** 获取状态对应的颜色（用于 Ant Design Tag 组件） */
export function getStatusColor(status: DocumentStatus): string {
    return STATUS_COLORS[status]
}

