# Programming Symbols

Most programming languages build their syntax from the same small set of keyboard symbols. The same symbol usually means the same thing from one language to the next, but not always: `//` divides in Python and starts a comment in C#, and `^` is exclusive or, not a power, in nearly every language. This page is a quick reference for reading code. Your book's chapters give the exact rules for its language.

The **Where** column uses these groups:

- **C family**: C, C++, C#, Java, and JavaScript, which share most of their operators.
- **Python**.
- **Shell**: Bash and other POSIX shells.

```{contents}
:local:
:depth: 2
```

```{index} programming symbols
```

```{index} arithmetic operators
```

## Arithmetic Operators

| Symbol | Meaning | Where |
| --- | --- | --- |
| `+` | Addition; also joins strings in most languages | All |
| `-` | Subtraction; also negation (`-x`) | All |
| `*` | Multiplication | All |
| `/` | Division | All |
| `%` | Remainder (modulus) | All |
| `**` | Exponent (`2 ** 3` is 8) | Python, JavaScript, Shell arithmetic |
| `//` | Floor division (`7 // 2` is 3) | Python only |

Division depends on the operand types. In the C family, dividing two integers drops the fraction, so `7 / 2` is `3`. In Python, `/` always produces a floating-point result (`3.5`), and `//` gives the floor. Languages without `**` use a library call such as `Math.Pow` (C#) or `Math.pow` (Java).

```{index} assignment operator; compound assignment
```

## Assignment Operators

| Symbol | Meaning | Equivalent to |
| --- | --- | --- |
| `=` | Assign | `x = 5` |
| `+=` | Add and assign | `x = x + 5` |
| `-=` | Subtract and assign | `x = x - 5` |
| `*=` | Multiply and assign | `x = x * 5` |
| `/=` | Divide and assign | `x = x / 5` |
| `%=` | Remainder and assign | `x = x % 5` |
| `**=` | Exponent and assign (Python, JavaScript) | `x = x ** 5` |
| `//=` | Floor divide and assign (Python) | `x = x // 5` |

A single `=` assigns; it does not compare. Writing `=` where you meant `==` is one of the most common beginner errors.

```{index} increment operator; prefix and postfix
```

## Increment and Decrement

| Symbol | Meaning | Where |
| --- | --- | --- |
| `++` | Add 1 | C family |
| `--` | Subtract 1 | C family |

`x++` (postfix) produces the old value and then increments; `++x` (prefix) increments first. Python has neither operator; write `x += 1`.

```{index} comparison operator; equality
```

## Comparison Operators

| Symbol | Meaning | Where |
| --- | --- | --- |
| `==` | Equal to | All languages (Shell: inside `[[ ]]`) |
| `!=` | Not equal to | All languages (Shell: inside `[[ ]]`) |
| `>` | Greater than | All |
| `<` | Less than | All |
| `>=` | Greater than or equal to | All |
| `<=` | Less than or equal to | All |
| `===`, `!==` | Equal (or not) without type conversion | JavaScript |

Equality has language-specific traps. In Java, `==` on objects such as strings compares references; use `.equals()` to compare contents. In Python, `is` tests whether two names refer to the same object, while `==` compares values. In shell tests, `-eq`, `-lt`, and `-gt` compare numbers, and `<` and `>` compare strings.

```{index} logical operator; short-circuit evaluation
```

## Logical Operators

| C family and Shell | Python | Meaning |
| --- | --- | --- |
| `&&` | `and` | True when both sides are true |
| `\|\|` | `or` | True when either side is true |
| `!` | `not` | Reverses true and false |

Both forms short-circuit: the right side is evaluated only when the left side does not already decide the result. In the shell, `cmd1 && cmd2` runs `cmd2` only if `cmd1` succeeds, and `cmd1 || cmd2` runs it only if `cmd1` fails.

```{index} membership operator
```

## Membership Operators

| Symbol | Meaning | Where |
| --- | --- | --- |
| `in` | Present in a collection | Python |
| `not in` | Not present in a collection | Python |

`3 in [1, 2, 3]` is `True`, and `"a" in "cat"` is `True`. C family languages use a method instead, such as `Contains` (C#), `contains` (Java), or `includes` (JavaScript).

```{index} bitwise operator; shift operators
```

## Bitwise Operators

| Symbol | Meaning | Where |
| --- | --- | --- |
| `&` | Bitwise AND | All languages |
| `\|` | Bitwise OR | All languages |
| `^` | Bitwise exclusive OR (XOR) | All languages |
| `~` | Bitwise NOT (flip every bit) | All languages |
| `<<` | Shift bits left | All languages |
| `>>` | Shift bits right | All languages |
| `>>>` | Shift right, filling with zeros | Java, JavaScript, C# |

Bitwise operators work on the individual bits of integers. Do not confuse them with the logical operators: `&&` and `||` combine true/false values, while `&` and `|` combine bits.

```{index} conditional operator
```
```{index} null operators
```

## Conditional Expressions

A conditional expression chooses between two values in a single expression.

| Form | Where |
| --- | --- |
| `condition ? value_if_true : value_if_false` | C family |
| `value_if_true if condition else value_if_false` | Python |

Two related operators handle missing (null) values in C# and JavaScript:

| Symbol | Meaning | Example |
| --- | --- | --- |
| `??` | Use the right side when the left is null | `name ?? "guest"` |
| `?.` | Access a member only when the object is not null | `user?.Email` |

```{index} delimiters; brackets and quotes
```

## Delimiters

| Symbol | Name | Common uses |
| --- | --- | --- |
| `( )` | Parentheses | Grouping, function calls, conditions in C family `if` and `while` |
| `[ ]` | Square brackets | Indexing, arrays, lists; shell tests (`[ ]`, `[[ ]]`) |
| `{ }` | Curly braces | Code blocks (C family); dictionaries and sets (Python); object literals (JavaScript) |
| `< >` | Angle brackets | Generic types such as `List<int>` (C#, Java, C++); HTML tags |
| `;` | Semicolon | Ends a statement (C family); separates commands on one line (Shell) |
| `,` | Comma | Separates arguments, parameters, and items |
| `.` | Dot | Member access (`obj.name`); decimal point |
| `:` | Colon | Starts an indented block (Python); labels and `switch` cases (C family) |
| `" "` | Double quotes | Strings; in the shell, variables inside still expand |
| `' '` | Single quotes | Strings (Python, JavaScript, Shell); one character in C, C++, C#, and Java |

In the shell, `'$HOME'` prints the text `$HOME`, while `"$HOME"` prints your home directory. In C# and Java, `'a'` is a `char` and `"a"` is a `string`.

```{index} comments; syntax by language
```
```{index} escape sequence
```

## Comments and Escapes

| Symbol | Meaning | Where |
| --- | --- | --- |
| `//` | Comment to end of line | C family |
| `/* ... */` | Block comment | C family |
| `#` | Comment to end of line | Python, Shell |
| `"""..."""` | Docstring (documentation string) | Python |
| `\` | Escape character: `\n` newline, `\t` tab, `\\` backslash, `\"` quote | All |

```{index} lambda expression
```
```{index} decorator
```
```{index} annotation
```

## Other Symbols

| Symbol | Meaning | Where |
| --- | --- | --- |
| `->` | Lambda (Java); member access through a pointer (C, C++); return type annotation (Python) | Varies |
| `=>` | Lambda or arrow function; expression-bodied member | C#, JavaScript |
| `...` | Spread or rest (JavaScript); variable-length arguments (Java); the `Ellipsis` placeholder (Python) | Varies |
| `#` | Preprocessor directive such as `#include` (C, C++) or `#if` (C#) | C, C++, C# |
| `@` | Decorator (Python); annotation such as `@Override` (Java); verbatim string `@"C:\temp"` (C#) | Varies |
| `$` | Variable expansion such as `$HOME` | Shell |
| `$"..."` | Interpolated string | C# |
| `` `...${x}` `` | Template string with interpolation | JavaScript |
| `f"...{x}"` | Formatted string (f-string) | Python |
| `_` | Leading underscore marks a name as internal; a lone `_` is a value you ignore (C# discard); digit separator in `1_000_000` | Python, C#, Java |
| `\|` | Pipe: send one command's output to the next command | Shell |
| `&` | Run a command in the background (Shell); address-of (C, C++) | Varies |

In regular expressions, symbols take on yet another set of meanings: `^` matches the start of a line and `$` the end. Read a symbol in the context of the language or tool you are using.

```{index} programming symbols; reading code
```

## Reading a Line of Code

The same small program in a C family language and in Python shows most of the symbols on this page.

```java
if (a >= b && b != 0) {
    c = a + b;
    arr[i] = c * 2;
} else {
    c = a % b;   // remainder
}
```

```python
if a >= b and b != 0:
    c = a + b
    arr[i] = c * 2
else:
    c = a % b    # remainder
```

Parentheses group the condition, `&&` and `and` join two comparisons, braces or a colon with indentation mark each block, square brackets index into `arr`, and `//` or `#` starts a comment. The C family version ends each statement with a semicolon; Python ends it with a line break.

```{index} programming symbols; common mix-ups
```

## Common Mix-ups

- **`=` versus `==`**: `=` assigns a value; `==` compares two values.
- **`^` is not a power**: `2 ^ 3` is 1 (bitwise XOR). Use `**` or a library power function.
- **`//` in two languages**: floor division in Python, a comment in the C family.
- **Integer division**: `7 / 2` is 3 in the C family when both operands are integers.
- **`&` versus `&&`**: use `&&` (or `and`) to combine conditions; `&` works on bits.
- **Quote types**: single and double quotes are interchangeable in Python and JavaScript, but not in C#, Java, or the shell.

Before proceeding, find three symbols on this page that mean something different in your book's language than in another language you know, and write a one-line example of each in your language.
