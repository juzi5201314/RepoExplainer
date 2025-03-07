### 文件说明：Unix 特定信号处理模块

#### 文件路径
explanations/tokio/tokio/src/signal/unix.rs

#### 主要功能
该文件为 Tokio 异步运行时提供了 Unix 系统上的信号处理功能，允许程序以异步方式监听和响应操作系统信号（如 SIGINT、SIGTERM 等）。通过封装底层信号注册和事件循环机制，为用户提供流式接口。

---

#### 核心组件

1. **信号类型定义 (`SignalKind`)**
   - 表示 Unix 信号的枚举类型，通过 `libc` 映射到具体信号编号（如 `SIGINT` 对应 Ctrl+C）
   - 提供 `from_raw` 和 `as_raw_value` 方法实现与原始信号值的转换
   - 预定义常见信号（如 `interrupt()`、`terminate()` 等）

2. **信号存储 (`OsStorage`)**
   - 使用 `Box<[SignalInfo]>` 存储所有信号的元数据
   - 实现 `Init` 初始化时根据操作系统类型确定信号范围（普通信号 1-33，Linux 还包含实时信号）
   - 通过 `Storage` trait 提供事件信息查询和遍历接口

3. **信号处理机制**
   - **全局信号处理器 (`action` 函数)**：
     - 标记信号事件
     - 通过 Unix 套接字对 (`UnixStream`) 向事件循环发送唤醒信号
   - **信号启用 (`signal_enable` 函数)**：
     - 注册信号处理器，确保每个信号仅注册一次
     - 使用 `signal_hook_registry` 实现安全的信号注册

4. **信号监听器 (`Signal` 结构体)**
   - 基于 `RxFuture` 实现异步流接口
   - 提供 `recv` 方法等待信号事件，支持 `async/await` 和 `poll_recv` 手动轮询
   - 通过 `signal` 函数创建监听器，内部调用 `signal_with_handle` 初始化信号注册

5. **辅助组件**
   - **Unix 套接字管道 (`OsExtraData`)**：
     - 使用 `UnixStream` 对实现线程间通信，用于信号事件的异步唤醒
   - **原子操作与同步**：
     - 使用 `AtomicBool` 和 `Once` 确保信号初始化的安全性

---

#### 工作流程
1. **初始化**：
   - 通过 `OsStorage::init` 预分配所有可能信号的元数据
   - 创建 Unix 套接字对用于信号事件的跨线程通信

2. **信号注册**：
   - 调用 `signal(SignalKind)` 创建监听器时，触发 `signal_enable` 注册信号处理器
   - 注册成功后，将监听器订阅到全局事件通知系统

3. **信号触发**：
   - 当操作系统发送信号时，全局处理器 `action` 被调用
   - 标记信号事件并写入套接字唤醒事件循环

4. **事件处理**：
   - 事件循环检测到套接字数据后，通知所有订阅该信号的监听器
   - 监听器通过 `recv` 方法异步获取信号事件

---

#### 项目中的角色