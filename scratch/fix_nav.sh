#!/bin/bash

# Files to update
files=(
    "Teacher/course.html"
    "Teacher/announcements.html"
    "Teacher/learn.html"
    "Teacher/calendar.html"
    "Teacher/course-details.html"
    "Student/is-coral-animal.html"
    "Student/announcements.html"
    "Student/messages.html"
    "Student/learn.html"
    "Student/calendar.html"
    "Student/profile.html"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "Updating $file..."
        # Use sed to remove .nav-links { display: none; } block from 1280px media query
        # and add new 600px media query
        
        # This sed command is a bit complex for multiline. 
        # I'll use a simpler approach: replace the closing brace of the 1280px block 
        # if it's preceded by .nav-links { display: none; }
        
        sed -i '' '/.nav-links {/,/}/d' "$file"
        
        # Add the 600px query before the </style> tag
        sed -i '' 's/<\/style>/    @media (max-width: 600px) {\n      .nav-links {\n        display: none;\n      }\n    }\n  <\/style>/' "$file"
    else
        echo "File $file not found."
    fi
done
