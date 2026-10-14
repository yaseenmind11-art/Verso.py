
def local_reference_similarity_scan(text: str, reference_files):
    """
    Compare writing against reference files locally.

    No external API or per-scan service quota.
    Coverage is limited to the reference documents provided.
    """
    def normalize(value):
        return re.sub(r"\W+", " ", value.casefold()).strip()

    sentences = [
        re.sub(r"\s+", " ", sentence).strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if len(re.findall(r"\w+", sentence)) >= 7
    ]

    references = []

    for uploaded_file in reference_files or []:
        try:
            content = extract_text(uploaded_file)
            if content.strip():
                references.append({
                    "name": uploaded_file.name,
                    "text": content,
                    "sentences": [
                        normalize(s)
                        for s in re.split(r"(?<=[.!?])\s+", content)
                        if normalize(s)
                    ],
                })
        except Exception:
            continue

    matches = []

    for sentence in sentences:
        best_match = None
        normalized_sentence = normalize(sentence)

        for reference in references:
            similarity = max(
                (
                    difflib.SequenceMatcher(
                        None,
                        normalized_sentence,
                        reference_sentence,
                    ).ratio()
                    for reference_sentence in reference["sentences"]
                ),
                default=0.0,
            )

            overlap = ngram_overlap(
                sentence,
                reference["text"],
                n=4,
            )

            score = max(similarity * 100, overlap)

            if best_match is None or score > best_match["score"]:
                best_match = {
                    "reference": reference["name"],
                    "similarity": round(similarity * 100, 1),
                    "overlap": round(overlap, 1),
                    "score": score,
                }

        if best_match and (
            best_match["similarity"] >= 55
            or best_match["overlap"] >= 15
        ):
            matches.append({
                "sentence": sentence,
                **best_match,
            })

    matches.sort(key=lambda item: item["score"], reverse=True)

    return {
        "reference_count": len(references),
        "sentences_checked": len(sentences),
        "matches": matches,
    }
