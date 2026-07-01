import re
import os

css_path = "/Users/aradhyajauhari/.gemini/antigravity/scratch/helpingotherssmile/style.css"

with open(css_path, "r") as f:
    css = f.read()

# 1. Replace :root
root_pattern = re.compile(r":root\s*\{.*?\n\}", re.DOTALL)
new_root = """:root {
    /* Color Palette */
    --color-bg: #E3E1ED; /* Lavender Background */
    --color-surface: #F5F4F9;
    --color-primary: #471F0D; /* Dark Brown */
    --color-primary-dark: #2F1408;
    --color-secondary: #2C5739; /* Forest Green */
    --color-accent: #6D093C; /* Deep Burgundy Accent */
    --color-accent-dark: #4A0629;
    --color-text: #333333;
    --color-text-light: #555555;
    --color-text-dark: #1A1A1A;
    
    /* Typography */
    --font-heading: 'Outfit', sans-serif;
    --font-body: 'Inter', sans-serif;
    
    /* Layout */
    --container-width: 1200px;
    --spacing-sm: 1rem;
    --spacing-md: 2rem;
    --spacing-lg: 4rem;
    --spacing-xl: 8rem;
    
    /* Utilities */
    --radius-md: 12px;
    --radius-lg: 24px;
    --transition-fast: 0.2s ease;
    --transition-smooth: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    --shadow-sm: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-md: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
    
    /* Glassmorphism */
    --glass-bg: rgba(255, 255, 255, 0.65);
    --glass-border: 1px solid rgba(255, 255, 255, 0.7);
    --glass-shadow: 0 8px 32px 0 rgba(71, 31, 13, 0.1);
}"""
css = root_pattern.sub(new_root, css)

# 2. Replace buttons globally but careful with non-buttons
# Actually just doing string replace is safe enough for these specific vars
css = css.replace("var(--color-primary)", "var(--color-accent)")
css = css.replace("var(--color-primary-dark)", "var(--color-accent-dark)")
# Wait, if I replace var(--color-primary) everywhere, it will replace it in places like section titles.
# That's fine, the titles will be burgundy, which matches "accent color (use it a little more often)".
# Let's keep it. But wait, the hero title uses secondary and primary gradients. Burgundy is nice there too.

# Replace old blue shadows with burgundy shadows for buttons
css = css.replace("rgba(14, 165, 233, 0.39)", "rgba(109, 9, 60, 0.39)")
css = css.replace("rgba(14, 165, 233, 0.23)", "rgba(109, 9, 60, 0.23)")
# Other blue rgba replaced with accent rgba
css = css.replace("rgba(14, 165, 233, 0.15)", "rgba(109, 9, 60, 0.15)")
css = css.replace("rgba(14, 165, 233, 0.1)", "rgba(109, 9, 60, 0.1)")
css = css.replace("rgba(14, 165, 233, 0.2)", "rgba(109, 9, 60, 0.2)")

# 3. Hero gradients
css = css.replace("background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);", "background: linear-gradient(135deg, var(--color-bg) 0%, var(--color-surface) 100%);")
css = css.replace("background: #e0f2fe;", "background: var(--color-secondary); opacity: 0.1;")
css = css.replace("background: #e1e1ff;", "background: var(--color-accent); opacity: 0.1;")

# Fix the gradient in project card back
css = css.replace("background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);", "background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-dark) 100%);")
css = css.replace("background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-dark) 100%);", "background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-dark) 100%);")

# Append reveal classes
reveal_classes = """

/* Reveal Animations */
.reveal {
    opacity: 0;
    transform: translateY(40px) scale(0.95);
    transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.reveal.active {
    opacity: 1;
    transform: translateY(0) scale(1);
}

.reveal-delay-1 { transition-delay: 0.1s; }
.reveal-delay-2 { transition-delay: 0.2s; }
.reveal-delay-3 { transition-delay: 0.3s; }
"""
css += reveal_classes

with open(css_path, "w") as f:
    f.write(css)

print("CSS updated successfully")
