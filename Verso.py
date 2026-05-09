# --- MODULE 4: CITATION HELPER (Scribbr Style) ---
elif choice == "📚 Citation Helper":
    st.title("Scribbr-Style Citation Generator")
    st.markdown('<div class="instruction-box">"Generate accurate APA 7th Edition citations for your research sources."</div>', unsafe_allow_html=True)
    
    # Input Area
    source_url = st.text_input("🔗 Paste the source URL here:", placeholder="https://www.nature.com/articles/s41586-024-00000-x")
    
    col1, col2 = st.columns(2)
    with col1:
        author = st.text_input("👤 Author(s):", placeholder="e.g., Smith, J., & Doe, A.")
    with col2:
        title = st.text_input("📄 Article/Page Title:", placeholder="e.g., The Impact of Climate Change")

    pub_date = st.text_input("📅 Publication Date:", placeholder="e.g., 2024, May 8")
    site_name = st.text_input("🏛️ Website/Journal Name:", placeholder="e.g., National Geographic")

    if st.button("Generate APA Citation"):
        if source_url or title:
            st.divider()
            st.subheader("Your APA Citation")
            
            # Formatting logic to mimic Scribbr's precision
            today = datetime.date.today().strftime("%Y, %B %d")
            
            # Constructing the citation string
            # Format: Author. (Date). Title. Site Name. URL.
            final_author = author if author else "Anonymous"
            final_date = f"({pub_date})" if pub_date else "(n.d.)"
            final_title = f"*{title}*" if title else "*Untitled Source*"
            final_site = f". {site_name}" if site_name else ""
            
            full_citation = f"{final_author}. {final_date}. {final_title}{final_site}. {source_url}"
            
            # Display in a professional "Scribbr" style result box
            st.markdown(f"""
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; color: #1e293b;">
                    <p style="margin-bottom: 10px; font-weight: bold; color: #3b82f6;">APA 7th Edition:</p>
                    <p style="font-family: 'Courier New', monospace; font-size: 1.1rem;">{full_citation}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.button("📋 Copy to Clipboard (Simulated)")
            st.success("Citation generated successfully!")
        else:
            st.error("Please provide at least a URL or a Title to generate a citation.")
