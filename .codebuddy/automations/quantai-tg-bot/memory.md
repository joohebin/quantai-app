# QuantAI TG Bot 运行记录

## 2026-03-30 03:40
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-30 07:01
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-30 08:02
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-30 12:30
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-30 13:31
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-30 15:34
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-30 16:37
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-31 05:30
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-31 06:31
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-31 10:58
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-31 14:25
- 检查状态：发现 2 个 tg_support_bot.py 进程在运行（PID 33460, 41664）
- 操作：无需启动
- 状态：正常运行

## 2026-03-31 15:27
- 检查状态：未发现 tg_support_bot.py 进程运行
- 操作：后台启动 TG Bot
- 启动命令：Start-Process with hidden window
- 启动结果：成功（新 PID 已生成）
- 状态：已重启

## 2026-03-31 18:54
- 检查状态：发现 3 个 tg_support_bot.py 进程在运行（PID 33460, 41664, 36408）
- 操作：无需启动
- 状态：正常运行

## 2026-04-01 19:25
- 检查状态：未发现 tg_support_bot.py 进程运行
- 操作：后台启动 TG Bot
- 启动命令：Start-Process with hidden window
- 启动结果：Bot 启动后连接 Telegram 服务器失败（httpx.ConnectTimeout）
- 错误原因：无法连接到 Telegram API，网络超时
- 状态：启动失败（网络问题）

## 2026-04-01 21:30
- 检查状态：未发现 tg_support_bot.py 进程运行
- 操作：后台启动 TG Bot
- 启动命令：Start-Process with hidden window
- 启动结果：Bot 启动后连接 Telegram 服务器失败（httpx.ConnectTimeout）
- 错误原因：无法连接到 Telegram API，网络超时
- 状态：启动失败（网络问题）

## 2026-04-01 23:35
- 检查状态：未发现 tg_support_bot.py 进程运行
- 操作：后台启动 TG Bot（PID 33780）
- 启动命令：Start-Process with hidden window
- 启动结果：成功。Bot 成功连接 Telegram API（getMe, setMyCommands, deleteWebhook 均返回 HTTP 200 OK），Scheduler 和 Application 已正常启动
- 状态：正常运行

## 2026-04-01 22:32
- 检查状态：未发现 tg_support_bot.py 进程运行
- 操作：按计划后台启动 TG Bot
- 启动结果：进程启动后很快退出，未保持运行
- 原因摘要：连接 Telegram API 超时（httpx.ConnectTimeout）
- 状态：启动失败（网络问题）

## 2026-04-02 00:36
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 33780，自 4/1 23:35 启动）
- 操作：无需启动
- 状态：正常运行

## 2026-04-02 01:37
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 33780）
- 操作：无需启动
- 状态：正常运行

## 2026-04-02 05:04
- 检查状态：未发现 tg_support_bot.py 进程运行
- 操作：后台启动 TG Bot（PID 39060）
- 启动结果：成功。Bot 成功连接 Telegram API（getMe, setMyCommands, deleteWebhook 均返回 HTTP 200 OK），Scheduler 和 Application 已正常启动，getUpdates 轮询正常
- 状态：正常运行

## 2026-04-02 08:31
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 39060，自 4/2 05:04 启动）
- 操作：无需启动
- 状态：正常运行

## 2026-04-02 12:38
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 39060，自 4/2 05:04 启动）
- 操作：无需启动
- 状态：正常运行

## 2026-04-02 13:41
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 39060，自 4/2 05:04 启动）
- 操作：无需启动
- 状态：正常运行

## 2026-04-02 21:14
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 30856，自 4/2 20:12 启动）
- 操作：无需启动
- 状态：正常运行
- 检查状态：未发现 tg_support_bot.py 进程运行
- 操作：后台启动 TG Bot（PID 30856）
- 启动结果：成功。Bot 成功连接 Telegram API（getMe, setMyCommands, deleteWebhook 均返回 HTTP 200 OK），Scheduler 和 Application 已正常启动
- 状态：正常运行

## 2026-04-02 22:15
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 30856，自 4/2 20:13 启动）
- 操作：无需启动
- 状态：正常运行（getUpdates 轮询正常，HTTP 200 OK）

## 2026-04-02 16:45
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 39060，自 4/2 05:04 启动）
- 操作：无需启动
- 状态：正常运行

## 2026-04-03 02:49
- 检查状态：未发现 tg_support_bot.py 进程运行（上次实例 PID 30856 已退出）
- 操作：后台启动 TG Bot（PID 14740）
- 启动命令：Start-Process with hidden window
- 启动结果：成功。Bot 成功连接 Telegram API（getMe, setMyCommands, deleteWebhook 均返回 HTTP 200 OK），Scheduler 和 Application 已正常启动，getUpdates 轮询正常
- 状态：正常运行

## 2026-04-03 01:46
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 30856，自 4/2 20:13 启动）
- 操作：无需启动；巡检过程中误拉起 1 个重复实例（PID 38512）后已立即停止
- 状态：正常运行（当前保留单实例 PID 30856）

## 2026-04-03 23:30
- 检查状态：未发现 tg_support_bot.py 进程运行
- 操作：后台启动 TG Bot
- 启动命令：Start-Process with hidden window
- 启动结果：Bot 进程启动，但连接 Telegram API 超时（httpcore.ConnectTimeout → telegram.error.TimedOut）
- 错误原因：无法连接到 Telegram API 服务器，网络超时
- 状态：启动失败（网络问题）
- 备注：这是 4/1 以来第 3 次因网络超时启动失败，4/2 20:12 曾短暂成功（PID 30856）

## 2026-04-04 19:21
- 检查状态：未发现 tg_support_bot.py 进程运行
- 操作：后台启动 TG Bot（PID 26360）
- 启动命令：Start-Process with hidden window
- 启动结果：成功。Bot 成功连接 Telegram API（getMe, setMyCommands, deleteWebhook 均返回 HTTP 200 OK），Scheduler 和 Application 已正常启动
- 状态：正常运行
- 备注：网络问题已恢复，Bot 正常启动并保持运行

## 2026-04-04 23:50
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 26360，自 4/4 19:21 启动）
- 操作：无需启动
- 状态：正常运行

## 2026-04-05 00:53
- 检查状态：未发现 tg_support_bot.py 进程运行（上次实例 PID 26360 已退出）
- 操作：后台启动 TG Bot（PID 39512）
- 启动命令：Start-Process with hidden window
- 启动结果：成功。Bot 成功连接 Telegram API（getMe, setMyCommands, deleteWebhook 均返回 HTTP 200 OK），Scheduler 和 Application 已正常启动，getUpdates 轮询正常
- 状态：正常运行

## 2026-04-05 01:55
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 39512，自 4/5 00:53:50 启动）
- 操作：无需启动
- 状态：正常运行（getUpdates 轮询正常，HTTP 200 OK，日志持续记录中）

## 2026-04-05 02:56
- 检查状态：发现 tg_support_bot.py 进程正在运行（PID 39512）
- 操作：无需启动
- 状态：正常运行


































