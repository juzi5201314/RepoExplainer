### 文件说明：时间抽象源代码（clock.rs）

#### 文件目的
该文件为 Tokio 的时间模块提供了时间抽象实现。主要功能包括：
1. 默认情况下使用 `std::time::Instant` 提供系统时间
2. 当启用 `test-util` 特性时，提供可配置的时间控制功能（暂停/恢复/跳跃时间）
3. 支持测试环境下的时间模拟，便于异步代码的测试验证

#### 核心组件

##### 1. 时间抽象结构（Clock）
```rust
pub(crate) struct Clock {
    inner: Mutex<Inner>,
}
```
- **Inner 结构体**：
  ```rust
  struct Inner {
      enable_pausing: bool,          // 是否启用暂停功能
      base: std::time::Instant,      // 基准时间点
      unfrozen: Option<Instant>,     // 未冻结时的当前时间起点
      auto_advance_inhibit_count: usize, // 自动推进抑制计数器
  }
  ```
- **关键方法**：
  - `pause()`：冻结时间，停止时间流动
  - `resume()`：恢复时间流动
  - `advance(duration)`：向前跳跃指定时间
  - `now()`：获取当前时间（考虑冻结状态）

##### 2. 时间控制函数
```rust
pub fn pause();          // 全局暂停时间
pub fn resume();         // 全局恢复时间
pub async fn advance();  // 异步时间跳跃
```
- 需要 Tokio 的 `current_thread` 运行时支持
- 提供测试场景下精确控制时间流动的能力

##### 3. 特性条件编译
```rust
// 非测试环境
cfg_not_test_util! {
    // 简单实现，直接使用系统时间
}

// 测试环境
cfg_test_util! {
    // 完整的时间控制实现
}
```
通过 `cfg` 宏实现特性驱动的代码分支：
- 默认模式：最小化实现，无额外开销
- 测试模式：启用完整的时间控制功能

##### 4. 时间访问机制
```rust
pub(crate) fn now() -> Instant {
    if !DID_PAUSE_CLOCK.load(Ordering::Acquire) {
        return std::time::Instant::now().into();
    }
    // 使用自定义时钟逻辑
}
```
- 使用原子标志 `DID_PAUSE_CLOCK` 优化判断路径
- 在未使用测试功能时直接调用系统时间

#### 运行时集成
- 通过 `with_clock` 函数获取当前运行时的时钟实例：
  ```rust
  fn with_clock<R>(f: impl FnOnce(Option<&Clock>) -> Result<R, &'static str>) -> R { ... }
  ```
- 支持多线程安全访问（通过 `Mutex`）
- 与 Tokio 运行时的 `Handle` 紧密集成

#### 项目中的角色
该文件是 Tokio 时间模块的核心实现，提供：
1. 生产环境下的基础时间服务
2. 测试环境下的时间控制能力（支持 `tokio::test` 宏）
3. 时间流动的灵活管理（暂停/恢复/跳跃）
4. 通过条件编译平衡测试功能与生产性能
