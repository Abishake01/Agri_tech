 
# Smart Farming Advisor 🌱🎙️

An AI-powered agricultural assistant that helps farmers with crop recommendations and water management through voice and text interactions.

![Project Screenshot](/static/images/screenshot.png)

## Features

- **Voice & Text Input** 🎤✍️  
  Ask questions naturally or type your queries
- **Crop Recommendations** 🌾  
  Get personalized crop suggestions based on:
  - Current season
  - Soil type
  - Weather conditions
  - Water availability
- **Water Management** 💧  
  Calculate:
  - Well water capacity
  - Drainage times
  - Irrigation schedules
- **3D Visualization** 📊  
  Interactive well and water level models
 

## Installation

### Prerequisites
- Python 3.8+
- Node.js (for frontend assets)
- PostgreSQL (recommended)

### Setup
1. Clone the repository:
   ```
   git clone https://github.com/Abishake01/smart-farming-advisor.git
   cd smart-farming-advisor
   ```

2. Set up virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
 
4. Database setup:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```

## Running the Project

1. Start development server:
   ```
   python manage.py runserver
   ```

2. Collect static files:
   ```
   python manage.py collectstatic
   ```

3. Access the application:
   ```
   http://localhost:8000
   ```

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Maintainer - [Your Name](mailto:your.email@example.com)  
Project Link: [https://github.com/Abishake01/smart-farming-advisor](https://github.com/Abishake01/smart-farming-advisor)
```

Would you like me to add any specific deployment instructions or additional configuration details?