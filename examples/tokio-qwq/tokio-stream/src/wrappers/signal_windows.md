### 文件目的
该文件为 Tokio 框架在 Windows 平台上的控制信号（Ctrl+C 和 Ctrl+Break）提供了基于 `Stream` 特性的封装，使开发者能够通过流式接口异步处理这些系统信号。

---

### 核心组件

#### 1. **CtrlCStream**
- **结构体**：`CtrlCStream { inner: CtrlC }`
  - 封装了 Tokio 的 `CtrlC` 类型，用于监听 Ctrl+C 信号。
- **关键方法**：
  - `new(interval: CtrlC) -> Self`：构造函数，将原始信号句柄包装为流。
  - `into_inner`：获取内部原始的 `CtrlC` 对象。
  - `poll_next`：实现 `Stream` 特性，通过 `poll_recv` 检查是否有新信号事件。
- **功能**：将 Tokio 的 `CtrlC` 适配为符合 `Stream` 特性的异步流。

#### 2. **CtrlBreakStream**
- **结构体**：`CtrlBreakStream { inner: CtrlBreak }`
  - 封装了 Tokio 的 `CtrlBreak` 类型，用于监听 Ctrl+Break 信号。
- **关键方法**：
  - `new(interval: CtrlBreak) -> Self`：构造函数，包装原始信号句柄。
  - `into_inner`：获取内部原始的 `CtrlBreak` 对象。
  - `poll_next`：通过 `poll_recv` 检查信号事件。
- **功能**：将 Tokio 的 `CtrlBreak` 转换为 `Stream` 接口。

#### 3. **通用特性实现**
- **`Stream` 特性**：
  - `type Item = ()`：信号事件无有效载荷，仅表示事件发生。
  - `poll_next` 方法直接委托给内部信号对象的 `poll_recv`。
- **`AsRef` 和 `AsMut`**：
  - 提供对底层 Tokio 信号对象的引用访问，保持灵活性。

---

### 工作原理
1. **信号监听初始化**：
   - 调用 Tokio 的 `ctrl_c()` 或 `ctrl_break()` 获取原始信号句柄。
2. **流封装**：
   - 通过 `CtrlCStream::new()` 或 `CtrlBreakStream::new()` 将句柄包装为流。
3. **异步处理**：
   - 使用 `StreamExt` 的 `next()` 方法在异步循环中等待信号事件。
   - 每次信号触发时，流会生成一个 `()` 值，表示事件发生。

---

### 项目中的角色