# 文件说明：tokio/src/time/interval.rs

## 文件目的
该文件实现了 Tokio 异步运行时中的定时器功能，提供基于间隔时间的异步周期性任务支持。通过 `Interval` 结构体和相关方法，开发者可以创建可配置的周期性定时任务，并处理因任务延迟导致的“错过 tick”情况。

---

## 核心组件

### 1. **Interval 结构体**
```rust
pub struct Interval {
    delay: Pin<Box<Sleep>>,
    period: Duration,
    missed_tick_behavior: MissedTickBehavior,
    // tracing 相关字段（可选）
}
```
- **功能**：管理周期性定时任务的核心结构体
- **关键字段**：
  - `delay`: 使用 `Sleep` 实现的异步等待句柄
  - `period`: 定时器间隔时长
  - `missed_tick_behavior`: 处理错过 tick 的策略（Burst/Delay/Skip）

### 2. **MissedTickBehavior 枚举**
```rust
pub enum MissedTickBehavior {
    Burst,
    Delay,
    Skip,
}
```
- **作用**：定义定时器错过预定 tick 时的处理策略：
  - **Burst（默认）**：立即连续触发所有错过的时间点，尽快追上
  - **Delay**：从当前时间重新计算周期，避免累积延迟
  - **Skip**：跳过所有错过的时间点，等待下一个预定时间点

### 3. **关键函数**
```rust
pub fn interval(period: Duration) -> Interval
pub fn interval_at(start: Instant, period: Duration) -> Interval
```
- **interval**: 创建立即开始的周期定时器
- **interval_at**: 创建指定起始时间的周期定时器
- **特性**：
  - 参数校验：`period` 必须大于 0，否则 panic
  - 使用 `internal_interval_at` 内部方法初始化定时器

---

## 核心逻辑

### 1. **tick 方法**
```rust
pub async fn tick(&mut self) -> Instant {
    poll_fn(|cx| self.poll_tick(cx)).await
}
```
- **功能**：等待直到下一个预定时间点到达
- **实现**：
  - 通过 `poll_tick` 检查当前时间是否达到预定时间
  - 返回预定时间点（非实际触发时间）

### 2. **poll_tick 方法**
```rust
pub fn poll_tick(&mut self, cx: &mut Context<'_>) -> Poll<Instant> {
    // 等待当前 delay 完成
    ready!(Pin::new(&mut self.delay).poll(cx));

    // 根据是否错过 tick 决定下一个时间点
    let next = if now > timeout + 5ms {
        self.missed_tick_behavior.next_timeout(...)
    } else {
        timeout + period
    };

    self.delay.reset_without_reregister(next);
    Poll::Ready(timeout)
}
```
- **核心逻辑**：
  1. 检查当前时间是否超过预定时间 + 5ms（判断是否"错过"）
  2. 根据策略计算下一个 tick 时间
  3. 重置延迟等待器，准备下次触发

### 3. 重置方法
```rust
pub fn reset(&mut self) { ... }
pub fn reset_immediately(&mut self) { ... }
pub fn reset_after(&mut self, after: Duration) { ... }
pub fn reset_at(&mut self, deadline: Instant) { ... }
```
- 提供多种方式重置定时器，忽略当前 missed_tick 策略

---

## 使用示例
```rust
// 创建每10ms触发的定时器
let mut interval = time::interval(Duration::from_millis(10));

// 第一个 tick 立即触发
interval.tick().await;

// 设置错过 tick 处理策略
interval.set_missed_tick_behavior(MissedTickBehavior::Skip);

// 在循环中使用
for _ in 0..5 {
    interval.tick().await;
    // 执行耗时操作
}
```

---

## 在项目中的角色