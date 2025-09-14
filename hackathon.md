
🌴 Poke MCP Challenge

Hi! We're The Interaction Company of California, the team behind Poke. You may have seen our recent launch video or better yet, given automations a try. We're sponsoring HackMIT this weekend, and in the spirit of open collaboration, wanted to extend the challenge to both hackers and global Poke enthusiasts alike!

We're giving away various iPhone 17 Pro/Air devices, Meta Raybans, Apple AirPods Pro 3, exclusive Interaction × The North Face jackets and tees, and all-expenses-paid trips to California for the winning teams! Multiple prize categories are available for both HackMIT participants and the broader community.
Challenge:

So what are Poke Automations? Poke Automations are custom actions that can be triggered by incoming emails or scheduled to occur. Users can use automations to send emails, schedule meetings, be reminded to drink water, or even water their plants! For more examples, check out our automations gallery.

We challenge you to build automations of your own! You can start here, or from scratch! Feel free to explore adjacent projects like agentic interfaces or any other innovative ideas, the wackier the better.
Submissions:

In order to be considered for all prizes, teams must submit your automations here by 11:45 AM EDT / 8:45 AM PDT on Sunday, September 14th. Participants from HackMIT are considered for the grand prize through the HackMIT submission process, but are welcome to enter for all other prizes through this form as well.
Prizes:

    Best MCP Automation (open to HackMIT participants only):
        Prize: iPhone 17 Pro or Air (one per team member) + Interaction × The North Face jackets and tees + all-expenses-paid trip to the San Francisco Bay Area for the entire winning team
        Description: Overall best automation open to HackMIT participants only. Visit The Interaction Company of California's home state for a weekend, and feel free to stay for an additional week with your friends.
    Most Technically Impressive MCP Automation:
        Prize: iPhone 17 Pro + Interaction × The North Face jackets + California trip
        Description: Most technically impressive automation judged on technical complexity, e.g. elaborate MCP connections, API integrations, novel use of MCP, etc.
    Most Fun MCP Automation:
        Prize: Meta Raybans + Apple AirPods Pro 3 + Interaction × The North Face jackets + California trip
        Description: Most fun/creative automation as measured by total social media views and user engagement (across platforms) on your demo.
    Most Practical MCP Automation:
        Prize: iPhone Air + Interaction × The North Face jackets + California trip
        Description: Most useful automation judged by the Interaction team based on how many people would want to add it from the automations gallery.

How to Add Your New MCP to Poke

Want to integrate your Model Context Protocol (MCP) server with Poke?

    Go to https://poke.com/settings/connections/integrations/new to add your MCP integration
    Use our verified MCP server template with 1-click deploy: https://github.com/InteractionCo/mcp-server-template
    **If needed, ask us to disable the bouncer for your account**

The template repository is pre-configured and verified to work seamlessly with Poke, making it easy to get started with your custom MCP implementation!
How to Send Messages to Poke

To send messages to Poke programmatically:

    Create an API key at https://poke.com/settings/advanced
    Make a POST request to the Poke API with your API key and message

Examples:
Bash

API_KEY="your-api-key-here"
MESSAGE="Hello from HackMIT!"

response=$(curl 'https://poke.com/api/v1/inbound-sms/webhook' \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -X POST \
        -d "{\"message\": \"$MESSAGE\"}")

echo $response

TypeScript

const API_KEY = 'your-api-key-here';
const MESSAGE = 'Hello from HackMIT!';

const response = await fetch('https://poke.com/api/v1/inbound-sms/webhook', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: MESSAGE })
});

const data = await response.json();
console.log(data);

Python

import requests

API_KEY = 'your-api-key-here'
MESSAGE = 'Hello from HackMIT!'

response = requests.post(
    'https://poke.com/api/v1/inbound-sms/webhook',
    headers={
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    },
    json={'message': MESSAGE}
)

print(response.json())

If you're also at HackMIT this weekend, feel free to stop by our booth with any questions (or just to say hi!). If you're interested in joining our team in building products for a billion humans, apply at interaction.co/jobs. Otherwise, reach out to us at hi@interaction.co or Twitter. Can't wait to see what you build!

With love,
The Interaction Team 🌴
