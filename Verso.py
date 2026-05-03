with tab1:
    query = st.text_input("What are we researching today?", placeholder="Ask a complex question...", key="main_search")
    
    if query:
        st.markdown(f"### ⚡ Analysis: {query}")
        
        st.markdown(f"""
            <div class='result-card'>
                <strong style='color: #00a1ff;'>📊 Executive Summary</strong><br><br>
                Searching global databases for <b>"{query}"</b>. 
                Below are the most relevant academic and verified sources found for your IB project.
            </div>
            """, unsafe_allow_html=True)

        # This creates dynamic links based on your search
        search_query = query.replace(" ", "+")
        
        trusted, other = st.columns(2)
        with trusted:
            st.markdown("#### ✅ Academic Sources")
            st.markdown(f"* **[Google Scholar Results](https://scholar.google.com/scholar?q={search_query})**")
            st.markdown(f"* **[CORE Academic Search](https://core.ac.uk/search?q={search_query})**")
        with other:
            st.markdown("#### 🌐 Encyclopedia & News")
            st.markdown(f"* **[Britannica Search](https://www.britannica.com/search?query={search_query})**")
            st.markdown(f"* **[Reuters Archive](https://www.reuters.com/site-search/?query={search_query})**")
