# 自定义执行器与Tokio集成示例

## 功能概述
该代码示例演示了如何在自定义线程池执行器中集成Tokio运行时，实现非Tokio主线程环境下的异步任务执行。通过创建自定义执行器，可以在保持原有执行环境的同时，运行Tokio的异步IO操作。

## 核心组件解析

### 1. 自定义执行器模块 `my_custom_runtime`
```rust
mod my_custom_runtime {
    // ...
}
```
- **ThreadPool结构体**：
  ```rust
  struct ThreadPool {
      inner: futures::executor::ThreadPool,
      rt: tokio::runtime::Runtime,
  }
  ```
  - `futures::executor::ThreadPool`：标准线程池，用于调度用户任务
  - `tokio::runtime::Runtime`：单线程Tokio运行时，处理IO驱动和上下文切换

- **静态执行器实例**：
  ```rust
  static EXECUTOR: Lazy<ThreadPool> = Lazy::new(|| {
      let rt = tokio::runtime::Builder::new_multi_thread()
          .enable_all()
          .build().unwrap();
      let inner = futures::ThreadPool::builder().create().unwrap();
      ThreadPool { inner, rt }
  });
  ```
  - 使用`once_cell`确保单例实例
  - 启动支持IO和定时器的Tokio多线程运行时
  - 创建标准线程池用于任务调度

- **任务调度方法**：
  ```rust
  impl ThreadPool {
      fn spawn(&self, f: impl Future<Output = ()> + Send + 'static) {
          let handle = self.rt.handle().clone();
          self.inner.spawn_ok(TokioContext::new(f, handle));
      }
  }
  ```
  - 使用`TokioContext`包装任务，确保在Tokio上下文中执行
  - 通过标准线程池调度任务执行

### 2. 主函数逻辑
```rust
fn main() {
    let (tx, rx) = oneshot::channel();

    my_custom_runtime::spawn(async move {
        let listener = TcpListener::bind("0.0.0.0:0").await.unwrap();
        println!("addr: {:?}", listener.local_addr());
        tx.send(()).unwrap();
    });

    futures::executor::block_on(rx).unwrap();
}
```
- 使用`oneshot`通道同步任务完成状态
- 在自定义执行器中启动TCP监听器绑定任务
- 主线程通过阻塞等待任务完成

## 技术关键点
1. **上下文切换**：通过`TokioContext`确保异步任务在Tokio运行时上下文中执行
2. **资源隔离**：Tokio运行时运行在独立线程，避免与自定义执行器直接冲突
3. **混合执行**：允许在标准线程池中调度Tokio任务，同时保持原有执行环境

## 项目角色