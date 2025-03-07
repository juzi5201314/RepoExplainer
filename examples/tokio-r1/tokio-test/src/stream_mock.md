# StreamMock Implementation in Tokio-Test

## Purpose
This file provides a mock implementation of a [`Stream`] for testing asynchronous code that interacts with streams. The `StreamMock` allows precise control over stream behavior, including item emission timing and sequence, enabling deterministic testing of stream consumers.

## Key Components

### 1. Action Enum
```rust
enum Action<T: Unpin> {
    Next(T),
    Wait(Duration),
}
```
Defines possible stream actions:
- `Next`: Emits a value
- `Wait`: Introduces a delay before next item

### 2. StreamMockBuilder
```rust
pub struct StreamMockBuilder<T: Unpin> {
    actions: VecDeque<Action<T>>,
}
```
Builder pattern for creating configured streams with:
- Method chaining (`next()`, `wait()`)
- Action queue management
- Final `build()` method to create StreamMock

### 3. StreamMock Implementation
```rust
pub struct StreamMock<T: Unpin> {
    actions: VecDeque<Action<T>>,
    sleep: Option<Pin<Box<Sleep>>>,
}
```
Implements `Stream` with:
- Time-aware polling using Tokio's `Sleep`
- State management between item emission and waiting periods
- Automatic cleanup verification on drop

## Key Features
- **Deterministic Timing**: Simulates precise delays between items using Tokio's time system
- **Consumption Safety**: Panics if unconsumed `Next` actions remain when dropped
- **Async Integration**: Properly implements wake mechanics for async runtime integration
- **Test Flexibility**: Supports complex stream behavior sequencing through builder pattern

## Usage Example
```rust
let mut stream_mock = StreamMockBuilder::new()
    .next(1)
    .wait(Duration::from_millis(300))
    .next(2)
    .build();
```
Creates a stream that:
1. Immediately emits 1
2. Waits 300ms
3. Emits 2
4. Terminates

## Integration with Project
This implementation serves as a testing utility within the Tokio ecosystem, specifically for:
- Validating stream consumer implementations
- Testing time-sensitive stream processing logic
- Creating controlled scenarios for async code verification
- Complementing Tokio's testing facilities with stream-specific mocking capabilities

## Quality Assurance
The `Drop` implementation ensures test reliability by:
```rust
assert!(undropped_count == 0, "...");
```
Guarding against unconsumed items in tests through runtime verification.

This file provides a configurable stream mock implementation for testing asynchronous stream processing logic in Tokio-based applications.  