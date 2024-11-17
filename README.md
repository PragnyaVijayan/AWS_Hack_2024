# Ascend
by Tiffany Nguyen, Lindsey Leong, Pragnya Vijayan, Maddie Follosco, Irene Chang, and Lydia Martin

## Inspiration
Imagine a world where freelancers are empowered to focus on their craft, while AI takes care of the arduous tasks of analyzing contracts, understanding market trends, and negotiating optimal terms. Ascend levels the playing field, ensuring freelancers are not undervalued while fostering transparency and efficiency in client negotiations.

## What it does
### Ascend's key features include:
1. Market Rate Analysis: Our product will compare the freelancer’s requested rates against market data so the user can gauge how well they're being paid. This includes a summary section that uses Hugging Face's bart-large-cnn to pull main points from lengthy contracts the user can upload, a graph that pulls salary data for the user's occupation and location from CareerOneStop's API and compares that to what the user is being offered, and a graph that visualizes the user's current pay with their pay history. When the user uses our product, their data is stored in AWS S3.

2. Support Real-Time Negotiation: The AI will initiate conversations with clients and suggest reasonable terms or counteroffers through the freelancer's email. GPT-3 powers chat-based interactions and automatically drafts as a response to emails from interested clients to cut down time for negotiation, though the user can review drafts before sending the messages themselves.

### Workflow
1. Freelancer Input: The freelancer provides data about themselves including their occupation, their location, the expected rate, and any contract terms they'd like to discuss.
2. Client Interaction: If the freelancer is in an ongoing negotiation, the AI uses GPT-3 to interface with the client by drafting emails the user can look over. It dynamically adjusts the conversation based on the client's responses, suggesting counteroffers, rate adjustments, and flexible terms.
3. Data Visualization Dashboard: Using the data the user provided about their job, location, and contract terms, AI summarizes the proposed contract for the user to look over and we pulls historical data from the CareerOneStop API to establish baseline market rates at various percentiles in the user's state. 

## How we built it
-** React JS** for our frontend
- **Python** and **Flask** for our backend.
- **Amazon S3** for our database
- AI
  - **Hugging Face **to parse/summarize contracts
  - **GPT-3** to draft negotiation emails
  - **Sagemaker** for personalized market analysis
- Data visualization
  - plots using **matplotlib**
  - Data from the **CareerOneStop API**
- **Figma** for design

## Challenges we ran into
Entering this hackathon, we knew that learning about the different AWS services and integrating them into our project would be a challenge, and it was. Everything took a lot of troubleshooting, researching, and plain old trying and trying again, but in the end, we were able to learn so much!

## Accomplishments that we're proud of
Working with AWS for the first time. Our resilience and debugging skills. Huge emphasis on resilience and debugging skills. 

## What's next for Ascend
Even though this hackathon has come to an end, we're definitely not done with Ascend! We'd love to broaden our customer base and specialize our data and models not only on the freelancer population, but extend our software to business contracts other licensing agreements, as legally binding contracts are everywhere and always relevant. We would also like to improve our model to extract more specific information from contracts such as wages or potential concerns to negotiate, along with providing more in-depth market analysis using user-specific data.

## Video Demo
You can find a full demo of Ascend [here](https://youtu.be/lm50RP4OufU)!

<img height="350" alt="Ascend home page" src="https://github.com/user-attachments/assets/d09e2688-3504-4edf-820d-810527be9c57">
<img height="350" alt="Data visualization" src="https://github.com/user-attachments/assets/00ff11c2-1b04-49f5-b93e-8e96e3128cb2">

## Summary
<img height="275" alt="Purpose" src="https://github.com/user-attachments/assets/0fc62640-7cf7-461a-ad2f-57e4eeb2e511">
<img height="275" alt="Workflow" src="https://github.com/user-attachments/assets/f2eafb58-8539-4c16-99d3-06ce5505653c">
