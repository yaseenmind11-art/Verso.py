elif choice == "⚙️ Settings":
    st.markdown('<h1 style="font-size: 3rem;">Verso Control Center</h1>', unsafe_allow_html=True)
    
    if st.button("🚨 MASTER RESET", type="primary", use_container_width=True): 
        trigger_master_reset()
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('### 📚 Academic & Audio')
        st.selectbox("Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
        if st.button("Test Tone"): components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
        
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
        
        st.selectbox("Tone Level", ["Formal", "Casual", "Academic"])
        st.radio("Complexity", ["Brief", "Standard", "Deep"], index=1)
        st.checkbox("Auto-Bibliography", value=True); st.checkbox("Logic Validation", value=True)
    with col2:
        st.markdown('### 🎨 UI Appearance')
        def update_accent(): st.session_state.set_color = st.session_state.accent_pick
        def update_bg(): st.session_state.set_bg = st.session_state.bg_pick
        st.color_picker("Accent Color", value=st.session_state.set_color, key="accent_pick", on_change=update_accent)
        st.color_picker("Card BG", value=st.session_state.set_bg, key="bg_pick", on_change=update_bg)
        st.slider("Font Scale", 0.8, 2.0, value=st.session_state.set_font, key="set_font")
        st.checkbox("Force Dark", value=True); st.checkbox("Glassmorphism")
    with col3:
        st.markdown('### 🔐 System Info')
        st.button("Purge History"); st.button("Export CSV"); st.button("Cloud Backup")
        st.info(f"Build: 14.5.6 (vID: {st.session_state.reset_counter})")
    st.success("System Optimized")

