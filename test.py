import google.generativeai as genai
genai.configure(api_key="AIzaSyBlvt3gzOt2N5HZa8YLDgpIvA8qJ3G-uJM")  # Test with a hardcoded key temporarily
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
print(model.generate_content("Hello").text)