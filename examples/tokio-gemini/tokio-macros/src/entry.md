这个文件 `src/entry.rs` 包含了用于 `tokio` 宏的核心逻辑，特别是 `#[tokio::main]` 和 `#[tokio::test]` 宏的实现。 它的主要目的是解析宏的参数，构建 `tokio` 运行时配置，并生成相应的代码来初始化和运行异步函数。

以下是该文件的关键组成部分：

1.  **`RuntimeFlavor` 枚举**: 定义了两种运行时模式：`CurrentThread`（单线程）和 `Threaded`（多线程）。
2.  **`UnhandledPanic` 枚举**: 定义了当异步任务发生未处理的 panic 时的行为：`Ignore`（忽略）和 `ShutdownRuntime`（关闭运行时）。
3.  **`FinalConfig` 结构体**: 存储最终的运行时配置，包括运行时模式、工作线程数量、是否启动暂停、crate 名称和未处理 panic 的行为。
4.  **`Configuration` 结构体**: 负责解析宏的参数，并构建运行时配置。 它包含各种设置方法，如 `set_flavor`、`set_worker_threads` 等，用于处理宏的属性参数。
5.  **`build_config` 函数**:  解析宏的参数，创建 `Configuration` 实例，并调用其方法来设置运行时配置。 它处理了参数的有效性检查和错误处理。
6.  **`parse_knobs` 函数**:  根据配置生成最终的代码。 它修改了输入函数的签名，添加了运行时初始化代码，并使用 `tokio` 运行时来运行异步函数。
7.  **`is_test_attribute` 函数**:  用于判断给定的属性是否是测试属性，例如 `#[test]`。
8.  **`main` 函数**:  处理 `#[tokio::main]` 宏。 它解析宏的参数，构建运行时配置，并生成相应的代码。
9.  **`test` 函数**:  处理 `#[tokio::test]` 宏。 它与 `main` 函数类似，但会添加测试相关的属性。
10. **`ItemFn` 结构体**:  用于解析和表示函数项，包括函数属性、签名、函数体等。
11. **`Body` 结构体**:  用于表示函数体，方便生成代码。
12. **辅助函数**:  包括 `parse_int`、`parse_string`、`parse_path` 和 `parse_bool` 等，用于解析宏的参数。

该文件通过解析宏的参数，构建 `tokio` 运行时配置，并生成相应的代码来初始化和运行异步函数，从而简化了用户编写异步代码的流程。
