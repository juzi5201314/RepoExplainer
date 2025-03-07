### 代码文件解释

#### 目的
该文件实现了 `StreamMock` 结构体及其构建器 `StreamMockBuilder`，用于模拟异步流的行为。它允许开发者在测试中精确控制流返回的值和等待时间，从而验证依赖流的代码逻辑。

#### 关键组件

1. **Action 枚举**
   - 定义流的行为类型：
     - `Next(T)`：表示流将返回一个值。
     - `Wait(Duration)`：表示流在返回下一个值前需要等待指定时长。

2. **StreamMockBuilder 构建器**
   - 通过链式调用配置流的行为：
     - `next(value)`：添加返回值动作。
     - `wait(duration)`：添加等待动作。
     - `build()`：生成最终的 `StreamMock` 实例。
   - 使用 `VecDeque` 存储按顺序执行的动作序列。

3. **StreamMock 结构体**
   - 实现 `futures_core::Stream` trait：
     - `poll_next` 方法按顺序处理动作：
       - `Next` 立即返回值。
       - `Wait` 使用 `tokio::time::sleep_until` 挂起当前任务，直到超时。
     - 内部通过 `sleep` 字段管理当前等待的定时器。
   - `Drop` trait 实现：确保所有配置的动作在流被销毁前均被处理，否则抛出错误。

#### 工作原理
1. **构建阶段**  
   通过 `StreamMockBuilder` 配置动作序列，例如：
   ```rust
   StreamMockBuilder::new().next(1).wait(Duration::from_millis(300)).next(2).build();
   ```

2. **执行阶段**  
   - 调用 `next().await` 触发动作处理：
     - 若当前动作是 `Next`，直接返回值。
     - 若是 `Wait`，挂起任务并等待指定时长。
   - 动作按队列顺序执行，所有动作完成后返回 `None`。

3. **错误检查**  
   在流被丢弃时检查是否所有 `Next` 动作均被消费，防止测试用例提前终止导致的未完成验证。

#### 项目中的角色