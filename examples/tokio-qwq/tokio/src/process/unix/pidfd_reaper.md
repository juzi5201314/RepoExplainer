# 文件说明：`tokio/src/process/unix/pidfd_reaper.rs`

## **文件目的**
该文件实现了基于Linux内核的`pidfd`机制的进程监控功能，用于异步等待子进程退出并处理僵尸进程。通过系统调用`pidfd_open`获取进程文件描述符，结合Tokio的事件循环实现非阻塞等待，同时确保进程资源的正确回收。

---

## **核心组件与功能**

### **1. `Pidfd`结构体**
- **作用**：封装进程的`pidfd`文件描述符，提供系统调用接口和事件注册能力。
- **关键方法**：
  - `open(pid: u32) -> Option<Pidfd>`：通过`syscall(SYS_pidfd_open)`获取进程的`pidfd`。若系统不支持（如返回`ENOSYS`错误），标记全局状态`NO_PIDFD_SUPPORT`为`true`，后续直接返回`None`。
  - 实现`AsRawFd` trait：暴露底层文件描述符，供事件循环注册使用。
  - 实现`mio::Source` trait：将`Pidfd`注册到Tokio的事件循环中，监听进程退出事件（可读事件）。

### **2. `PidfdReaperInner`结构体**
- **作用**：异步等待进程退出的核心Future实现。
- **关键特性**：
  - 包含`PollEvented<Pidfd>`用于事件驱动的IO操作。
  - `poll`方法通过`poll_read_ready`检测进程退出事件，成功后调用`try_wait()`获取退出状态。
  - 处理运行时关闭的异常情况，重新注册事件监听。

### **3. `PidfdReaper`结构体**
- **作用**：封装`PidfdReaperInner`并管理孤儿进程队列。
- **关键功能**：
  - **构造方法`new`**：尝试创建`Pidfd`，若成功则初始化异步Future，否则返回错误。
  - **`Drop` trait实现**：当`PidfdReaper`被销毁时，若进程未退出且未被等待，则将其加入`OrphanQueue`防止僵尸进程。
  - **`Kill` trait实现**：通过内部的`Wait`对象发送终止信号给进程。

### **4. 测试模块**
- **测试用例**：
  - `test_pidfd_reaper_poll`：验证异步等待进程退出的正确性。
  - `test_pidfd_reaper_kill`：测试终止进程的功能。
  - `test_pidfd_reaper_drop`：验证孤儿进程回收逻辑。
- **条件判断**：仅在Linux内核版本≥5.10（支持`pidfd`）时运行测试。

---

## **技术细节**
1. **系统调用**：通过`libc::syscall(SYS_pidfd_open)`获取`pidfd`，并设置`PIDFD_NONBLOCK`标志实现非阻塞。
2. **事件驱动**：利用`mio`库将`pidfd`注册到事件循环，通过`PollEvented`实现异步IO。
3. **僵尸进程处理**：通过`OrphanQueue`在`Drop`阶段回收未处理的进程，避免资源泄漏。
4. **错误处理**：检测系统不支持`pidfd`的情况，并全局缓存该状态以避免重复检查。

---

## **项目中的角色**