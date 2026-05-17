def correct_text(text):
    # Initialize the tool for US English
    tool = language_tool_python.LanguageTool('en-US')
    
    # Identify errors (grammar, spelling, punctuation, capitalization)
    matches = tool.check(text)
    
    # Automatically apply the suggested corrections
    corrected_text = tool.correct(text)
    
    return corrected_text, matches

# Example usage:
input_text = "this is a example of bad grammar and i forgot my punctuation"
corrected, errors = correct_text(input_text)

print(f"Original: {input_text}")
print(f"Corrected: {corrected}")
