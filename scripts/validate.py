    #!/usr/bin/env python3  
"""
Simple validator to test post metadata against filters.
Usage: python3 scripts/validate.py
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
filters_dir = BASE / "filters"
examples_dir = BASE / "examples"

def load_json(p):
    return json.loads(p.read_text(encoding="utf-8"))

def matches_any_tag(tag_list, blacklist):
    return any(t.lower() in (b.lower() for b in blacklist) for t in tag_list)

def main():
    tags = load_json(filters_dir / "tags.json")
    desc = load_json(filters_dir / "description_regex.json")
    alt = load_json(filters_dir / "alttext_rules.json")

    allow_re = re.compile(desc["allow_pattern"], re.IGNORECASE)
    block_re = re.compile(desc["block_pattern"], re.IGNORECASE)
    alt_required_re = re.compile(alt["required_pattern"], re.IGNORECASE)
    alt_block_re = re.compile(alt["blacklist_pattern"], re.IGNORECASE)

    for p in examples_dir.glob("*.json"):
        post = load_json(p)
        print(f"--- Testing {post.get('id','<unknown>')} ({p.name}) ---")
        tags_list = post.get("tags", [])
        description = post.get("description", "")
        alt_text = post.get("alt_text", "") or ""
        age_gated = post.get("age_gated", False)

        reasons = []
        verdict = "NEUTRAL"

        # Tag blacklist check
        if matches_any_tag(tags_list, tags["blacklist"]):
            verdict = "BLOCKED_BY_TAG_BLACKLIST"
            reasons.append("Tag blacklist match")
        # Description block check
        elif block_re.search(description):
            verdict = "BLOCKED_BY_DESCRIPTION"
            reasons.append("Description matched block pattern")
        else:
            # Allow check
            if allow_re.search(description) or any(t.lower() in (w.lower() for w in tags["whitelist"]) for t in tags_list):
                # Need age confirmation for adult content
                if age_gated or alt_required_re.search(description) or alt_required_re.search(alt_text):
                    if alt_block_re.search(alt_text):
                        verdict = "BLOCKED_BY_ALT_BLACKLIST"
                        reasons.append("Alt text matched alt blacklist")
                    else:
                        verdict = "ALLOWED"
                        reasons.append("Passed allow checks and age confirmation present")
                else:
                    verdict = "DEMOTED_MISSING_AGE_CONFIRM"
                    reasons.append("Allow matched but missing age confirmation (18+/adult)")
            else:
                verdict = "NEUTRAL_NO_MATCH"
                reasons.append("No allow or block matches; treat as neutral")

        print("Verdict:", verdict)
        for r in reasons:
            print(" -", r)
        print()

if __name__ == "__main__":
    main()
