这个文件定义了 `tokio` 运行时中用于处理进程的驱动程序 (`Driver`)。它的主要目的是在 Unix 平台上清理孤立的子进程。

**关键组件：**

*   `Driver` 结构体：
    *   `park`:  一个 `SignalDriver` 实例，负责处理信号相关的操作，例如唤醒。
    *   `signal_handle`:  一个 `SignalHandle` 实例，用于与信号驱动程序交互。
*   `Driver` 的方法：
    *   `new(park: SignalDriver) -> Self`:  构造函数，创建一个新的 `Driver` 实例。它接收一个 `SignalDriver` 实例作为参数，并从该实例获取一个 `SignalHandle`。
    *   `park(&mut self, handle: &driver::Handle)`:  调用 `park` 方法，将唤醒操作委托给内部的 `SignalDriver`，然后调用 `GlobalOrphanQueue::reap_orphans` 来清理孤立的子进程。
    *   `park_timeout(&mut self, handle: &driver::Handle, duration: Duration)`:  类似于 `park`，但设置了超时时间。它调用 `park_timeout` 方法，将唤醒操作委托给内部的 `SignalDriver`，然后调用 `GlobalOrphanQueue::reap_orphans` 来清理孤立的子进程。
    *   `shutdown(&mut self, handle: &driver::Handle)`:  调用 `shutdown` 方法，关闭内部的 `SignalDriver`。

**与其他组件的交互：**

*   `SignalDriver`:  `Driver` 依赖于 `SignalDriver` 来处理信号相关的操作，例如唤醒。
*   `GlobalOrphanQueue`:  `Driver` 使用 `GlobalOrphanQueue` 来清理孤立的子进程。在每次 `park` 或 `park_timeout` 调用后，都会调用 `GlobalOrphanQueue::reap_orphans`。
*   `driver::Handle`:  `Driver` 的 `park` 和 `park_timeout` 方法都接收一个 `driver::Handle` 作为参数，用于与运行时驱动程序交互。

**整体项目中的作用：**
