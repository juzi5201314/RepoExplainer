这个文件展示了如何在任何其他执行器中使用 Tokio 运行时。它利用了 `RuntimeExt` 特性，该特性提供了自定义运行时的功能。

**关键组件：**

1.  **`use` 语句:** 引入了必要的 Tokio 模块，包括网络 ( `TcpListener` )、运行时构建器 ( `Builder` )、单次发送通道 ( `oneshot` ) 和上下文扩展 ( `RuntimeExt` )。
2.  **`main` 函数:**
    *   创建了两个单次发送通道 (`tx`, `rx`)，用于在不同运行时之间进行同步。
    *   创建了两个 Tokio 运行时 (`rt1`, `rt2`)。
        *   `rt1` 使用 `Builder::new_multi_thread()` 构建，配置了 1 个工作线程，并且没有启用定时器。
        *   `rt2` 也使用 `Builder::new_multi_thread()` 构建，配置了 1 个工作线程，并启用了所有功能 (包括定时器)。
    *   `rt1.block_on(rt2.wrap(async move { ... }))`：
        *   `rt2.wrap()` 将一个异步闭包包装在 `rt2` 的上下文中。由于 `rt1` 没有启用定时器，如果直接在 `rt1` 中运行需要定时器的操作，会导致 panic。`wrap` 函数解决了这个问题，确保了异步操作在正确的运行时上下文中执行。
        *   `TcpListener::bind("0.0.0.0:0").await.unwrap()` 创建一个 TCP 监听器，并绑定到任意可用端口。
        *   `println!("addr: {:?}", listener.local_addr())` 打印监听器的本地地址。
        *   `tx.send(()).unwrap()` 通过单次发送通道发送一个信号，通知 `rt1` 中的操作已经完成。
    *   `futures::executor::block_on(rx).unwrap()` 阻塞当前线程，直到从 `rx` 接收到信号，从而确保程序在所有异步操作完成后退出。

**如何融入项目：**

这个文件展示了如何在 Tokio 中使用多个运行时，并处理运行时之间的依赖关系。这在需要自定义运行时配置，或者需要将 Tokio 与其他执行器集成时非常有用。`RuntimeExt` 提供了灵活的方式来管理和控制 Tokio 运行时。
