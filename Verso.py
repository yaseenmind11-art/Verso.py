# --- TAB 2: VERSO EDITOR (Fixed Logic) ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=250, key="v_editor_final")
    if user_text:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 🌐 Translator")
            target_lang = st.selectbox("Select Language:", ["arabic", "french", "spanish", "german"])
            if st.button("Translate Now"):
                st.info(GoogleTranslator(source='auto', target=target_lang).translate(user_text))
        with col_b:
            st.markdown("#### 📏 Grammar & Punctuation Fix")
            if st.button("Analyze & Correct"):
                # Initial cleaning
                input_text = user_text.strip()
                
                # Use TextBlob for spelling, but we'll add logic to protect questions
                blob = TextBlob(input_text)
                temp = str(blob.correct())
                
                # Fix punctuation spacing
                temp = re.sub(r'\s+([,.!?;:])', r'\1', temp)
                temp = re.sub(r'([,.!?;:])(?=[^\s\d])', r'\1 ', temp)
                
                # Sentence processing
                sentences = re.split(r'(?<=[.!?])\s+', temp)
                final_sentences = []
                for s in sentences:
                    if len(s) > 0:
                        s = s[0].upper() + s[1:]
                        # Fix "i" issues
                        s = s.replace(" i ", " I ").replace(" i'", " I'").replace(" i.", " I.")
                        
                        # LOGIC FIX: If the sentence starts with a question word but lacks a '?', add it
                        question_words = ['What', 'Who', 'Where', 'When', 'Why', 'How', 'Is', 'Are', 'Do', 'Does', 'Can']
                        if any(s.startswith(word) for word in question_words) and not s.endswith('?'):
                            if s.endswith('.'): s = s[:-1] # Remove period if it exists
                            s += '?'
                            
                        final_sentences.append(s)
                
                final_output = " ".join(final_sentences).strip()
                
                # IMPROVED COMPARISON: 
                # If the only difference is the punctuation you missed, it's a correction.
                # If the output is exactly what you wrote, trigger the celebration.
                if final_output == input_text:
                    st.balloons()
                    st.markdown('<div class="status-box">🎉 Congratulations! Your writing is perfect.</div>', unsafe_allow_html=True)
                else:
                    st.warning("Suggested Revision:")
                    st.success(final_output)
