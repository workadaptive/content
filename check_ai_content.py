"""
AI Content Detector for WorkAdaptive Content
Uses Originality.AI API to check if content reads as human-written

Setup:
1. Sign up at https://originality.ai/
2. Get your API key from the dashboard
3. Set environment variable: ORIGINALITY_API_KEY=your_key_here
   Or edit this script and paste your key in the api_key variable

Usage:
python check_ai_content.py
"""

import requests
import os
from pathlib import Path

# EDIT THIS: Paste your API key here or set ORIGINALITY_API_KEY environment variable
API_KEY = os.getenv('ORIGINALITY_API_KEY', 'your_api_key_here')

def check_ai_content(text, filename):
    """Check if text appears AI-generated using Originality.AI API"""
    
    url = "https://api.originality.ai/api/v1/scan/ai"
    headers = {"X-OAI-API-KEY": API_KEY}
    data = {"content": text, "aiModelVersion": "1"}  # Use latest model
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Extract scores
        ai_score = result.get("score", {}).get("ai", 0) * 100
        human_score = result.get("score", {}).get("original", 0) * 100
        
        # Determine verdict
        if human_score > 55:
            verdict = "✅ Human-likely"
            color = "green"
        elif human_score > 45:
            verdict = "⚠️  Mixed (borderline)"
            color = "yellow"
        else:
            verdict = "❌ AI-likely (needs humanization)"
            color = "red"
        
        return {
            "filename": filename,
            "ai_score": ai_score,
            "human_score": human_score,
            "verdict": verdict,
            "color": color,
            "word_count": len(text.split()),
            "success": True
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "filename": filename,
            "error": str(e),
            "success": False
        }

def main():
    """Check all WorkAdaptive content files"""
    
    print("=" * 70)
    print("AI Content Detection Report - WorkAdaptive")
    print("=" * 70)
    print()
    
    # Check if API key is set
    if API_KEY == 'your_api_key_here':
        print("⚠️  WARNING: API key not set!")
        print("Please set ORIGINALITY_API_KEY environment variable or edit this script")
        print()
        print("To set environment variable (PowerShell):")
        print('  $env:ORIGINALITY_API_KEY = "your_key_here"')
        print()
        return
    
    # Files to check
    files_to_check = [
        "why-ides-solve-ai-memory-problem.md",
        "four-phase-method-building-with-ai.md",
        "homepage-content.md",
        "services-content.md",
        "executive-messaging.md"
    ]
    
    results = []
    total_cost = 0
    
    for filename in files_to_check:
        filepath = Path(filename)
        
        if not filepath.exists():
            print(f"⚠️  File not found: {filename}")
            continue
        
        print(f"Checking: {filename}")
        
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check content
        result = check_ai_content(content, filename)
        
        if result["success"]:
            results.append(result)
            
            # Estimate cost (approximately $0.01 per 100 words)
            word_count = result["word_count"]
            cost = (word_count / 100) * 0.01
            total_cost += cost
            
            print(f"  Words: {word_count:,}")
            print(f"  AI Score: {result['ai_score']:.1f}%")
            print(f"  Human Score: {result['human_score']:.1f}%")
            print(f"  {result['verdict']}")
            print(f"  Cost: ${cost:.2f}")
        else:
            print(f"  ❌ Error: {result['error']}")
        
        print()
    
    # Summary
    if results:
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print()
        
        for result in results:
            status_icon = "✅" if result["human_score"] > 55 else "⚠️" if result["human_score"] > 45 else "❌"
            print(f"{status_icon} {result['filename']:<45} Human: {result['human_score']:.1f}%")
        
        print()
        print(f"Total estimated cost: ${total_cost:.2f}")
        print()
        
        # Recommendations
        needs_work = [r for r in results if r["human_score"] <= 55]
        if needs_work:
            print("RECOMMENDATIONS:")
            print()
            for result in needs_work:
                print(f"📝 {result['filename']}")
                print(f"   Current human score: {result['human_score']:.1f}%")
                print(f"   Target: >55% for safe publication")
                print()
                print("   Humanization techniques to try:")
                print("   - Add personal anecdotes and specific examples")
                print("   - Vary sentence length (mix short and long)")
                print("   - Use contractions (don't, can't, you're)")
                print("   - Include rhetorical questions")
                print("   - Add parenthetical asides")
                print("   - Inject opinion and personality")
                print()
        else:
            print("🎉 All content scores well! Ready for publication.")
            print()

if __name__ == "__main__":
    main()
