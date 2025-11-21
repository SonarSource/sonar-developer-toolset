---
name: java-unit-testing
description: Comprehensive Java unit testing guidelines using JUnit 5, Mockito, and AssertJ with consistent patterns, parameterized tests, nested organization, and 90%+ coverage standards.
---

# Java Unit Testing Best Practices

## Core Testing Framework Stack
- **JUnit 5** (Jupiter): Primary testing framework with @ExtendWith(MockitoExtension.class)
- **Mockito**: Mocking framework with field-level @Mock annotations and verification
- **AssertJ**: Fluent assertion library for readable test assertions

## Test Method Naming Conventions

### Primary Pattern: `methodName_condition_expectedBehavior`
```java
void authenticate_shouldReturnUserWhenValidCredentials()
void process_shouldThrowExceptionWhenInputIsNull()
void calculate_shouldReturnZeroWhenEmptyList()
```

### Alternative Pattern: `should` + `action` + `when/if` + `condition`
```java
void shouldReturnEmptyWhenNoDataFound()
void shouldThrowExceptionIfParameterInvalid()
void shouldProcessSuccessfullyWhenValidInput()
```

**Rule: Choose one pattern per test class and use it consistently**

## Text Block Usage

### Multi-line JSON/XML Content
```java
String jsonPayload = """
  {
    "id": "123",
    "type": "event",
    "data": {
      "status": "active"
    }
  }""";
```

### Multi-line Strings with Variables
```java
String expectedMessage = """
  Error processing request: %s
  Status: %s
  Timestamp: %s
  
  Please contact support if this persists.""".formatted(requestId, status, timestamp);
```

### SQL Queries and Complex Text
```java
String query = """
  SELECT u.id, u.name, p.title 
  FROM users u 
  JOIN projects p ON u.id = p.owner_id 
  WHERE u.active = true 
  AND p.created_date > ?""";
```

## Parameterized Tests

### @ParameterizedTest with @MethodSource for Complex Cases
```java
@ParameterizedTest
@MethodSource("validationTestCases")
void validate_shouldHandleVariousInputs(String input, boolean expectedValid, String expectedMessage) {
  ValidationResult result = validator.validate(input);
  
  assertThat(result.isValid()).isEqualTo(expectedValid);
  assertThat(result.getMessage()).isEqualTo(expectedMessage);
}

static Stream<Arguments> validationTestCases() {
  return Stream.of(
    Arguments.of("valid-input", true, "Input is valid"),
    Arguments.of("", false, "Input cannot be empty"),
    Arguments.of(null, false, "Input cannot be null")
  );
}
```

### @ParameterizedTest with @ValueSource for Simple Cases
```java
@ParameterizedTest
@ValueSource(strings = {"admin", "user", "guest"})
void shouldAcceptValidRoles(String role) {
  assertThat(roleValidator.isValid(role)).isTrue();
}

@ParameterizedTest
@ValueSource(ints = {1, 5, 10, 100})
void shouldCalculateCorrectly(int input) {
  assertThat(calculator.square(input)).isEqualTo(input * input);
}
```

## Nested Tests Organization

### Group by Feature/Operation
```java
@Nested
class CreateOperations {
  @BeforeEach
  void setUpCreate() {
    // shared setup for create tests
  }
  
  @Test
  void create_shouldReturnEntityWhenValidInput() {
    // test logic
  }
}

@Nested
class ValidationTests {
  @Test
  void validate_shouldRejectInvalidData() {
    // test logic
  }
}

@Nested
class ErrorHandling {
  @Test
  void process_shouldHandleExternalServiceFailure() {
    // test logic
  }
}
```

## Mock Setup Patterns

### Field-Level Mock Declaration
```java
@ExtendWith(MockitoExtension.class)
class ServiceTest {
  
  @Mock
  private Repository repository;
  @Mock
  private ExternalService externalService;
  @Mock
  private ValidationService validator;
  
  private ServiceUnderTest service;
  
  @BeforeEach
  void setUp() {
    service = new ServiceUnderTest(repository, externalService, validator);
  }
}
```

### Complete Mock Setup for Integration Testing
```java
@Test
void processRequest_shouldCompleteFullWorkflow() {
  when(validator.validate(any())).thenReturn(ValidationResult.valid());
  when(repository.save(any())).thenReturn(savedEntity);
  when(externalService.notify(any())).thenReturn(NotificationResult.success());
  
  ProcessResult result = service.processRequest(validRequest);
  
  assertThat(result.isSuccess()).isTrue();
  verify(validator).validate(validRequest);
  verify(repository).save(any());
  verify(externalService).notify(any());
}
```

## Assertion Patterns

### Basic AssertJ Assertions
```java
// Single property assertions
assertThat(result).isNotNull();
assertThat(result.getId()).isEqualTo(expectedId);
assertThat(result.isActive()).isTrue();
assertThat(optionalResult).isEmpty();

// Collection assertions
assertThat(list).hasSize(3);
assertThat(results).isEmpty();
assertThat(items).containsExactly(item1, item2, item3);
assertThat(set).containsExactlyInAnyOrder(itemA, itemB);
```

### Chain Assertions for Multiple Properties
```java
// Chain multiple assertions on the same object
assertThat(user)
  .extracting(User::getName, User::getEmail, User::isActive)
  .containsExactly("John Doe", "john@example.com", true);

// Chain assertions for object validation
assertThat(response)
  .isNotNull()
  .extracting(Response::getStatus, Response::getMessage)
  .containsExactly(Status.SUCCESS, "Operation completed");

// Chain assertions for collections with extraction
assertThat(users)
  .hasSize(2)
  .extracting(User::getName)
  .containsExactly("Alice", "Bob");
```

### Exception Assertions
```java
assertThatThrownBy(() -> service.process(invalidInput))
  .isInstanceOf(ValidationException.class)
  .hasMessage("Input validation failed")
  .hasMessageContaining("required field missing")
  .extracting(ValidationException::getErrorCode)
  .isEqualTo("VALIDATION_ERROR");
```

## Mock Verification Patterns

### Verify Specific Interactions
```java
// Verify method calls with specific parameters
verify(repository).save(eq(expectedEntity));
verify(externalService).notify(anyString(), eq(NotificationType.SUCCESS));

// Verify no unwanted interactions
verifyNoInteractions(unusedService);
verifyNoMoreInteractions(repository);

// Verify interaction counts
verify(cache, times(3)).get(anyString());
verify(validator, never()).validateExpensive(any());
```

### ArgumentCaptor for Complex Verification
```java
@Captor
private ArgumentCaptor<RequestDto> requestCaptor;

@Test
void shouldTransformDataCorrectly() {
  service.processData(inputData);
  
  verify(externalService).send(requestCaptor.capture());
  RequestDto capturedRequest = requestCaptor.getValue();
  
  assertThat(capturedRequest)
    .extracting(RequestDto::getType, RequestDto::getPriority)
    .containsExactly("PROCESS", Priority.HIGH);
}
```

## Code Coverage Guidelines

### Aim for 90%+ Coverage by Testing:

**Happy Path Scenarios**
- Valid inputs with successful processing
- Complete workflow execution
- Proper return values and state changes

**Input Validation and Edge Cases**
- Null/empty inputs
- Boundary values (min/max limits)
- Invalid formats or types
- Special characters and encoding

**Error Conditions**
- Exception handling and propagation
- External service failures
- Resource constraints (timeouts, limits)
- Invalid state transitions

**State Verification**
- Object property changes
- Side effects (database updates, file operations)
- Interaction with external systems
- Return type validation

### Skip These Cases:
- Simple getters/setters with no logic
- Auto-generated methods (equals, hashCode, toString)
- Unreachable defensive code paths
- Third-party library wrapper methods with no business logic

## Test Data Management

### Static Test Data
```java
private static final String VALID_EMAIL = "user@example.com";
private static final LocalDate TEST_DATE = LocalDate.of(2023, 1, 1);
```

### Test Data Builders
```java
private static class TestDataBuilder {
  static UserRequest validUserRequest() {
    return new UserRequest()
      .setName("John Doe")
      .setEmail("john@example.com")
      .setRole(Role.USER);
  }
  
  static UserEntity createUser(String name, String email) {
    UserEntity user = new UserEntity();
    user.setName(name);
    user.setEmail(email);
    user.setCreatedDate(LocalDateTime.now());
    return user;
  }
}
```

### Record Classes for Immutable Test Data
```java
private record TestScenario(
  String input,
  boolean shouldSucceed,
  String expectedError
) {}

private static final TestScenario INVALID_EMAIL = new TestScenario(
  "invalid-email", false, "Email format is invalid"
);
```

## Annotations Policy

### Avoid Unnecessary @DisplayName
```java
// Bad - method name already explains this
@Test
@DisplayName("should return sum when adding two positive numbers")
void should_returnSum_when_addingTwoPositiveNumbers() {
}

// Good - clear method name, no annotation needed
@Test
void should_returnSum_when_addingTwoPositiveNumbers() {
}
```

**Rule: Only use @DisplayName when method names cannot clearly express the test intent**

## Comments Policy

### Avoid Obvious Comments
```java
// Bad - method name already explains this
@Test
void shouldValidateEmail() {
  // Test validates email format
}

// Good - no comment needed  
@Test
void shouldValidateEmail() {
  // test implementation
}
```

### Add Comments for Complex Business Logic
```java
@Test
void shouldCalculateProRatedRefund() {
  // Business rule: Refund = (remaining_days / total_days) * amount - processing_fee
  // Processing fee is 5% minimum, capped at $50
  LocalDate subscriptionStart = LocalDate.of(2023, 1, 1);
  LocalDate cancellationDate = LocalDate.of(2023, 6, 15);
  
  Money refund = billingService.calculateRefund(subscription, cancellationDate);
  
  assertThat(refund).isEqualTo(Money.of(237.50)); // $500 * 0.5 * 0.95 = $237.50
}
```

### Add Comments for Test Data Context
```java
static Stream<Arguments> edgeCaseInputs() {
  return Stream.of(
    Arguments.of("", false, "Empty string not allowed"),
    Arguments.of("a".repeat(256), false, "Input exceeds max length"), // 256 chars > 255 limit
    Arguments.of("valid-input", true, null) // Happy path
  );
}
```

## Complete Test Class Template

```java
@ExtendWith(MockitoExtension.class)
class ServiceNameTest {

  @Mock
  private Repository repository;
  @Mock
  private ExternalService externalService;
  @Mock
  private ValidationService validator;
  
  @Captor
  private ArgumentCaptor<Entity> entityCaptor;

  private ServiceName underTest;

  @BeforeEach
  void setUp() {
    underTest = new ServiceName(repository, externalService, validator);
  }

  @Nested
  class CreateOperations {
    
    @Test
    void create_shouldReturnEntityWhenValidInput() {
      Entity expectedEntity = TestDataBuilder.createValidEntity();
      when(validator.validate(any())).thenReturn(ValidationResult.valid());
      when(repository.save(any())).thenReturn(expectedEntity);

      Entity result = underTest.create(validRequest);

      assertThat(result)
        .isNotNull()
        .extracting(Entity::getId, Entity::getStatus)
        .containsExactly(expectedEntity.getId(), Status.ACTIVE);
        
      verify(validator).validate(validRequest);
      verify(repository).save(entityCaptor.capture());
      assertThat(entityCaptor.getValue().getName()).isEqualTo(expectedEntity.getName());
    }

    @ParameterizedTest
    @MethodSource("invalidInputs")
    void create_shouldThrowExceptionWhenInputInvalid(Object invalidInput, String expectedMessage) {
      when(validator.validate(any())).thenReturn(ValidationResult.invalid(expectedMessage));

      assertThatThrownBy(() -> underTest.create(invalidInput))
        .isInstanceOf(ValidationException.class)
        .hasMessageContaining(expectedMessage);

      verify(validator).validate(invalidInput);
      verifyNoInteractions(repository);
    }

    static Stream<Arguments> invalidInputs() {
      return Stream.of(
        Arguments.of(null, "Input cannot be null"),
        Arguments.of("", "Input cannot be empty"),
        Arguments.of("   ", "Input cannot be blank")
      );
    }
  }

  @Nested  
  class ErrorHandling {
    
    @Test
    void process_shouldHandleRepositoryException() {
      when(repository.save(any())).thenThrow(new DataAccessException("Database error"));

      assertThatThrownBy(() -> underTest.process(validInput))
        .isInstanceOf(ProcessingException.class)
        .hasMessageContaining("Failed to save data")
        .hasCauseInstanceOf(DataAccessException.class);
    }
  }

  private static class TestDataBuilder {
    static Entity createValidEntity() {
      return new Entity("test-id", "Test Name", Status.ACTIVE);
    }
  }
}
```

## Best Practices Summary

1. **Use consistent naming patterns** within each test class
2. **Leverage text blocks** for multi-line strings and complex data
3. **Apply parameterized tests** to reduce duplication and increase coverage
4. **Organize with nested classes** for logical grouping of related tests
5. **Chain AssertJ assertions** when validating multiple properties
6. **Mock completely** for integration-style tests, minimally for unit tests  
7. **Verify interactions explicitly** - don't assume mocks were called correctly
8. **Aim for 90%+ coverage** by testing happy paths, edge cases, and error conditions
9. **Avoid unnecessary @DisplayName annotations** - let clear method names speak for themselves
10. **Avoid obvious comments** - let clear naming speak for itself
11. **Use test data builders** for complex object creation and reuse
