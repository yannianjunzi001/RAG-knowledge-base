import { message } from "antd"
import { client } from "@/client/client.gen" // <--- 从 client.gen 中导入 client 实例
import { formatApiError } from "@/utils/errors"

client.setConfig({
    baseUrl: '',
    throwOnError: true,
})

client.interceptors.response.use(async (response) => {
    if (!response.ok) {
        message.error(await formatApiError(response))
    }
    return response
})