### 文件说明：Tokio 运行时上下文管理模块

#### 文件目的
该文件实现了 Tokio 运行时中当前上下文（Context）的动态切换和管理机制。主要负责在多线程环境下安全地设置、获取和恢复运行时句柄（Handle），确保异步任务调度的正确性。

#### 核心组件

1. **SetCurrentGuard 结构体**
   - **作用**：通过 RAII 模式管理当前上下文的生命周期
   - **关键字段**：
     - `prev`：保存被替换前的 Handle
     - `depth`：记录当前嵌套层级深度
     - `_p`：防止跨线程移动的标记
   - **Drop 实现**：
     - 恢复之前的 Handle 状态
     - 验证层级深度是否匹配，防止 Guard 错误释放顺序

2. **HandleCell 结构体**
   - **作用**：存储当前 Handle 及嵌套深度计数器
   - **字段**：
     - `handle`：使用 RefCell 存储可变的 Handle（线程局部）
     - `depth`：使用 Cell 跟踪嵌套调用次数

3. **关键函数**
   - `try_set_current`：
     - 尝试将指定 Handle 设为当前活动句柄
     - 返回 Guard 对象以管理作用域
   - `with_current`：
     - 在当前上下文中执行闭包
     - 处理无上下文或线程局部存储损坏的错误
   - `Context::set_current`：
     - 替换当前 Handle 并更新嵌套深度
     - 使用断言防止层级溢出

#### 工作原理
1. **上下文切换流程**：
   - 调用 `try_set_current` 设置新 Handle 时，会保存旧值并增加嵌套深度
   - 通过 Guard 的 Drop 特性，在作用域结束时自动恢复旧状态
   - 使用线程局部存储（CONTEXT）确保每个线程独立维护自己的上下文

2. **嵌套保护机制**：
   - 通过 `depth` 字段跟踪嵌套层级
   - Drop 时验证层级一致性，防止 Guard 错误释放顺序导致的状态混乱

3. **错误处理**：
   - `with_current` 函数返回 Result 类型，明确区分三种错误场景：
     - 无当前上下文 (`TryCurrentError::NoContext`)
     - 线程局部存储被销毁 (`TryCurrentError::ThreadLocalDestroyed`)

#### 在项目中的角色