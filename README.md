# meakuchatbot_project

## Objective:

The objective of this document is to summarize the steps and learnings while working on the Meaku chatbot. The problem statement is to design an AI bot for the HackerEarth website that can effectively answer questions about the company, encourage users to sign up for a demo, ask relevant questions to carry longer conversations, show source link for the responses and capture their contact details for further follow-up. The bot could run on a local domain for now providing a good customer experience.

## Requirements:

1. **Bot Functionality:** Develop a conversational AI bot capable of:  
* Answering questions about HackerEarth, its products, services, and mission.  
* Providing information about available demos and their benefits.  
* Prompting users to sign up for a demo or contact HackerEarth for more details.  
* Ask relevant questions to users to carry longer conversations (aim for 4 min)  
* Show source URLs / docs so user can click and see where the given information was taken from (like perplexity)  
  
2. **User Engagement and Conversion:** Implement strategies to engage users effectively and convert their interest into action. This includes persuasive messaging, clear call-to-action prompts, and personalized responses tailored to user queries.  

3. **Data Capture and Storage:** Enable the bot to capture user contact details seamlessly. Upon user consent, collect information such as name, email address, company name, and any other relevant details. Utilize Google Sheets API or similar tools to securely store this data in a designated spreadsheet.  
   
4. **Content and Design Alignment:** Ensure that the bot's language, tone, and design align with HackerEarth's branding and communication guidelines. Maintain consistency with the website's overall look and feel to provide a cohesive user experience.

In this document, we summarize a demo version of an AI bot that would solve the problem of generating more relevant content during the conversations. We implement RAG on top of a base model from Ollama and talk about observed results and future possibilities for improvement.

## RAG implementation
## Interactive Dashboard using Panel

