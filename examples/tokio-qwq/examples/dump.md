### 文件说明

#### 目的
该文件是一个 Tokio 的示例程序，用于演示其实验性任务转储（task dump）功能。通过故意制造死锁场景，展示如何通过 `Ctrl+C` 触发任务跟踪信息的打印，帮助开发者诊断程序中的死锁问题。

#### 关键组件
1. **条件编译配置**  
   ```rust
   #[cfg(all(...))]
   ```
   仅在以下条件下编译：
   - 启用 `tokio_unstable` 和 `tokio_taskdump` 特性
   - 目标操作系统为 Linux
   - 目标架构为 `aarch64`、`x86` 或 `x86_64`

2. **死锁制造**  
   ```rust
   let barrier = Arc::new(Barrier::new(3));
   ```
   - 使用 `Barrier` 同步原语，设置需要 3 个任务同时到达才能继续
   - 但实际仅启动了两个任务（`task_1` 和 `task_2`），导致所有任务在 `barrier.wait().await` 处无限期等待

3. **信号处理函数 `dump_or_quit`**  
   ```rust
   async fn dump_or_quit() { ... }
   ```
   - 监听 `Ctrl+C` 信号：
     - 单次触发：执行任务转储，打印所有任务的调用栈信息
     - 双次触发（1秒内）：退出程序
   - 使用 `tokio::runtime::Handle::current().dump()` 获取任务转储数据
   - 若转储超时（2秒未完成），提示使用 `gdb` 等原生调试器

4. **任务链式调用**  
   ```rust
   async fn a(barrier: Arc<Barrier>) { b(barrier).await }
   async fn b(barrier: Arc<Barrier>) { c(barrier).await }
   async fn c(barrier: Arc<Barrier>) { barrier.wait().await }
   ```
   - 通过 `a -> b -> c` 的链式调用，形成清晰的任务调用栈，便于转储信息的可读性

5. **异步选择器 `tokio::select!`**  
   ```rust
   tokio::select! { ... }
   ```
   - 并行监听 `dump_or_quit`、`task_1` 和 `task_2` 的完成信号
   - 由于死锁，`task_1` 和 `task_2` 永远不会完成，程序依赖用户干预退出

#### 工作流程
1. 程序启动后提示用户操作：
   ```
   This program has a deadlock.
   Input CTRL+C to print a task dump.
   Input CTRL+C twice within 1 second to exit.
   ```

2. 当用户首次按下 `Ctrl+C`：
   - 触发任务转储，输出类似以下信息：
     ```
     TASK {id}:
     {调用栈跟踪}
     ```
   - 示例输出包含每个任务的 ID 和调用路径（如 `a -> b -> c -> barrier.wait()`）

3. 若用户在 1 秒内再次按下 `Ctrl+C`，程序立即退出。

#### 项目中的角色
该文件是 Tokio 的实验性功能示例，用于演示如何通过任务转储诊断死锁问题。它通过故意制造死锁场景，展示了 Tokio 在遇到复杂并发问题时的调试能力，帮助开发者理解如何利用 `tokio_taskdump` 特性定位程序阻塞原因。
