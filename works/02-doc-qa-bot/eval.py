"""Run the test questions against a PDF and score the answers.

Usage (from this folder):
    python eval.py sample-data/your-document.pdf tests/questions.csv

questions.csv columns:
    question        the question to ask
    expected_pages  page numbers that hold the answer, e.g. "3" or "3|4"; empty = answer is NOT in the document
    must_contain    words the answer must include, separated by "|"; "/" lists accepted
                    alternatives, e.g. "三十/30|书面"; may be empty

A question counts as correct when:
    in-document:      the bot answers, cites at least one expected page, and includes every must_contain word
    not in document:  the bot says it couldn't find the answer
Results go to docs/eval-results.csv. Check the failures by hand: a strict keyword can fail a good answer.
"""
import csv
import sys
from pathlib import Path

from rag import answer, build_index, load_pdf


def split(cell: str) -> list[str]:
    return [p.strip() for p in (cell or "").split("|") if p.strip()]


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("Usage: python eval.py <document.pdf> <questions.csv>")
    pdf, questions_csv = sys.argv[1], sys.argv[2]
    print("Indexing", pdf, "...")
    store = build_index(load_pdf(pdf))

    with open(questions_csv, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    results, correct = [], 0
    for i, row in enumerate(rows, 1):
        res = answer(store, row["question"])
        expected = {int(p) for p in split(row.get("expected_pages", ""))}
        words = split(row.get("must_contain", ""))
        if expected:
            ok = (res["found"]
                  and bool(expected & set(res["cited_pages"]))
                  and all(any(alt.lower() in res["answer"].lower() for alt in w.split("/"))
                          for w in words))
        else:
            ok = not res["found"]
        correct += ok
        print(f"{i:>2}. {'OK  ' if ok else 'FAIL'} {row['question'][:50]}")
        results.append({
            "question": row["question"],
            "expected_pages": row.get("expected_pages", ""),
            "cited_pages": "|".join(map(str, res["cited_pages"])),
            "correct": "yes" if ok else "no",
            "answer": res["answer"],
        })

    out = Path("docs/eval-results.csv")
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"\nScore: {correct} / {len(rows)}  ->  details in {out}")


if __name__ == "__main__":
    main()
