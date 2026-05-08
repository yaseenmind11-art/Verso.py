# --- MODULE 1: HOME (Updated Professional Search) ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown('<div class="instruction-box">"Select a module from the sidebar to start your academic workflow."</div>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Professional Academic Search:", placeholder="e.g., Climate change impact on Egypt")
    
    if st.button("Search Professional Results"):
        if search_query.strip():
            # This modified query forces Google to show only high-authority academic/gov sites
            professional_query = f"{search_query} site:.edu OR site:.gov OR site:.org OR site:.scholarpedia.org"
            q = professional_query.replace(' ', '+')
            
            st.info(f"Showing verified professional sources for: **{search_query}**")
            
            # Direct link to filtered Google results
            st.markdown(f"### [🚀 Click here for Professional Google Results](https://www.google.com/search?q={q})")
            
            st.divider()
            st.write("Specific Databases:")
            st.markdown(f"""
            * [Google Scholar: {search_query}](https://scholar.google.com/scholar?q={search_query.replace(' ', '+')})
            * [JSTOR Academic Archive](https://www.jstor.org/action/doBasicSearch?Query={search_query.replace(' ', '+')})
            """)
        else:
            st.warning("Please enter a research topic.")

# --- MODULE 6: TOOLS (Fixed Citation Assistant) ---
elif choice == "📚 Citation Helper":
    st.title("Citation Assistant")
    source_url = st.text_area("Paste source details or URL:", placeholder="https://www.britannica.com/search?query=hi")
    
    if st.button("Format"):
        if source_url:
            # Basic formatting logic
            st.subheader("Formatted Citation (APA 7th)")
            import datetime
            today = datetime.date.today().strftime("%Y, %B %d")
            
            # Simple automatic string builder
            citation = f"Source. ({today}). Retrieved from {source_url}"
            
            st.code(citation, language="text")
            st.success("Citation generated! Copy it into your bibliography.")
        else:
            st.error("Please paste a URL or source details first.")
