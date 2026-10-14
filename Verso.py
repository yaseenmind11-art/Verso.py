            with st.spinner("Processing context-aware translation..."):
                src_full = st.session_state.src_lang
                tgt_full = st.session_state.tgt_lang
                
                if client is not None:
                    system_instruction = f"""
                    You are a professional, exact translation assistant. Your task is to translate the user text from {src_full} to {tgt_full}.
                    Maintain exact meaning, tone, and punctuation structure.
                    Output ONLY the translated result text. Do not add any introductory or explanatory text.
                    """
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"Translate this text payload:\n\n{st.session_state.translator_input}",
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.3
                            )
                        )
                        st.session_state.translator_output = response.text.strip()
                        st.rerun()
                    except Exception as ai_err:
                        st.session_state.translator_output = "Translation could not be completed. Check the service connection and try again."
                else:
                    st.session_state.translator_output = "The translation service is not configured on this installation yet."

    with output_col:
        st.text_area(
            f"Translation in {st.session_state.tgt_lang}:",
            height=250,
            disabled=True,
            key="translator_output"
        )
        
# --- MODULE: SETTINGS ---
elif choice == "Settings":
    st.markdown('<h1 style="font-size: 2.4rem;">Verso Control Center</h1>', unsafe_allow_html=True)
    st.caption("Your original academic, audio, appearance, and system controls.")

    col1, col2, col3 = st.columns([1.05, 1.05, 0.9], gap="large")
    with col1:
        st.markdown('### Academic & Audio')
        st.selectbox("Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
        if st.button("Test Tone", use_container_width=True):
            components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)

        st.selectbox("Citation Style", [
            "APA 7th Generation",
            "APA 6th Generation",
            "APA 5th Generation",
            "MLA 9th Edition",
            "Chicago 17th (Notes & Bibliography)",
            "Chicago 17th (Author-Date)",
            "Harvard (Standard UK)",
            "Harvard (Australia)"
        ], key="selected_citation_format")
        st.selectbox("Tone Level", ["Formal", "Casual", "Academic"], key="tone_level")
        st.radio("Complexity", ["Brief", "Standard", "Deep"], key="complexity_level", horizontal=True)
        st.checkbox("Auto-Bibliography", key="auto_bibliography")
        st.checkbox("Logic Validation", key="logic_validation")

    with col2:
        st.markdown('### UI Appearance')
        def update_accent():
            st.session_state.set_color = st.session_state.accent_pick
        def update_bg():
            st.session_state.set_bg = st.session_state.bg_pick
        st.color_picker("Accent Color", value=st.session_state.set_color, key="accent_pick", on_change=update_accent)
        st.color_picker("Card BG", value=st.session_state.set_bg, key="bg_pick", on_change=update_bg)
        st.slider("Font Scale", 0.8, 2.0, value=st.session_state.set_font, key="set_font", step=0.05)
        st.checkbox("Force Dark", key="force_dark")
        st.checkbox("Glassmorphism", key="glassmorphism")

    with col3:
        st.markdown('### System Info')
        if st.button("Purge History", use_container_width=True):
            for key in ["plag_local_results", "plag_scan_results", "generated_lecture_text", "humanizer_output"]:
                st.session_state.pop(key, None)
            st.success("Temporary result history cleared.")
        if st.button("Export CSV", use_container_width=True):
            export_df = pd.DataFrame([
                {"setting": "Accent Color", "value": st.session_state.set_color},
                {"setting": "Card BG", "value": st.session_state.set_bg},
                {"setting": "Font Scale", "value": st.session_state.set_font},
                {"setting": "Alarm Tone", "value": st.session_state.selected_alarm_tone},
                {"setting": "Citation Style", "value": st.session_state.selected_citation_format},
                {"setting": "Tone Level", "value": st.session_state.tone_level},
                {"setting": "Complexity", "value": st.session_state.complexity_level},
                {"setting": "Auto-Bibliography", "value": st.session_state.auto_bibliography},
                {"setting": "Logic Validation", "value": st.session_state.logic_validation},
            ])
            st.download_button("Download settings CSV", export_df.to_csv(index=False).encode("utf-8"), "verso_settings.csv", "text/csv", use_container_width=True)
        if st.button("Cloud Backup", use_container_width=True):
            st.info("Cloud backup is not connected in this build. Use Export CSV to save your settings locally.")
        st.info(f"Build: 14.5.6 (vID: {st.session_state.reset_counter})")
        st.success("Workspace ready")

if st.session_state.get('timer_finished_trigger'):
    st.markdown('<div class="time-up-banner">Time is up</div>', unsafe_allow_html=True); st.balloons()
    components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
    if st.button("Dismiss Alarm"): st.session_state.timer_finished_trigger = False; st.rerun()
