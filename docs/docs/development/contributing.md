# Contributing Guide

## 📝 Documentation Style Guide

### Formatting Guidelines

1. **Markdown Usage**

   - Use standard GitHub-flavored Markdown
   - Do not use TeX-style math notation
   - For mathematical expressions, use plain text or code blocks

2. **Code Blocks**
   Use three backticks followed by the language name:

   ````
   ```python
   def example():
       return "Hello World"
   ```
   ````

3. **Headers**

   - Use ATX-style headers (`#` for h1, `##` for h2, etc.)
   - Include emojis in headers for visual organization
   - Keep header hierarchy (don't skip levels)

4. **Lists**

   - Use `-` for unordered lists
   - Use `1.` for ordered lists
   - Maintain consistent indentation (2 spaces)

5. **Tables**

   - Use standard Markdown tables
   - Include header row
   - Align columns appropriately

6. **Links**

   - Use relative paths for internal links
   - Use descriptive link text
   - Check links work in both development and production

7. **Images**

   - Store in the `images/` directory
   - Use descriptive alt text
   - Keep image sizes reasonable

8. **Mathematical Content**
   For mathematical expressions, use simple text formatting:
   ```
   BMI = weight (kg) / (height (m))²
   ```

### Examples

#### Mathematical Expressions

Good examples:

```
BMI = weight / (height * height)
Area = pi * r^2
```

#### Tables

```
| Category    | BMI Range   |
|-------------|------------|
| Underweight | < 18.5     |
| Normal      | 18.5-24.9  |
```

#### Code Examples

````
```python
def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height ** 2)
```
````

## 🔄 Pull Request Process

1. Create a new branch for your changes
2. Follow the documentation style guide
3. Test your changes locally using `mkdocs serve`
4. Submit a pull request with a clear description
5. Wait for review and address any feedback

## 🧪 Testing Documentation

Before submitting changes:

1. Run locally:

   ```
   mkdocs serve
   ```

2. Check:
   - All pages render correctly
   - Navigation works
   - Code blocks are properly formatted
   - Links work
   - Images display correctly

## 📋 Documentation Checklist

- [x] Follow style guide
- [x] Avoid TeX notation
- [x] Test all links
- [x] Check images
- [x] Format code blocks
- [x] Nest headers properly
- [x] Verify emoji rendering
- [x] Align tables
- [x] Check spelling and grammar
