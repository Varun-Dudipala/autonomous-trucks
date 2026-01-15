# Contributing to Autonomous Trucks Fleet Management System

Thanks for your interest in contributing to this fleet management system! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear, descriptive title
- Steps to reproduce the bug
- Expected vs actual behavior
- Screenshots if applicable (especially for UI bugs)
- Environment details (Python version, MongoDB version, OS, browser)
- Error messages or stack traces

### Suggesting Features

Feature requests are welcome! Please open an issue with:
- Clear description of the feature
- Use case explaining why it would be valuable for fleet management
- Any implementation ideas you have
- Consider scalability for large fleets

### Pull Requests

1. **Fork the repository** and create a new branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our code style guidelines

3. **Test your changes**
   - Test with local MongoDB
   - Verify all routes work correctly
   - Test with multiple users and trucks
   - Check responsive design on different screen sizes

4. **Commit your changes** with clear, descriptive messages
   ```bash
   git commit -m "Add: feature description"
   ```

5. **Push to your fork** and submit a pull request
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Describe your PR** with:
   - What changes you made
   - Why you made them
   - Any potential side effects
   - Screenshots for UI changes

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/autonomous-trucks.git
cd autonomous-trucks

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Ensure MongoDB is running
# macOS: brew services start mongodb-community
# Ubuntu: sudo systemctl start mongodb

# Run the app
python app.py
```

## Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and concise
- Use meaningful variable names

### Flask Routes
- Use RESTful conventions where possible
- Add `@login_required` decorator for protected routes
- Return appropriate HTTP status codes
- Use flash messages for user feedback
- Handle errors gracefully

### Templates
- Follow Jinja2 best practices
- Extend `base.html` for consistency
- Use semantic HTML5
- Keep CSS in `static/styles.css`
- Add comments for complex layouts

### Database
- Use descriptive collection and field names
- Validate data before database operations
- Handle MongoDB connection errors
- Consider indexing for frequently queried fields

### File Organization
- New routes in `app.py`
- Database models in `models.py`
- Database connection in `db.py`
- Templates in `templates/`
- Static files in `static/`

### Naming Conventions
- Functions: `snake_case` (e.g., `get_all_trucks()`)
- Classes: `PascalCase` (if added)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MONGODB_URI`)
- Templates: `lowercase_with_underscores.html`

### Code Quality
- Write clean, readable code
- Add comments for complex logic
- Remove debug print statements
- Handle edge cases (empty fleet, missing data)
- Validate user input

## Testing

### Manual Testing Checklist

Before submitting a PR, test these scenarios:

**Authentication:**
- [ ] Register new user
- [ ] Login with correct credentials
- [ ] Login with wrong credentials
- [ ] Access protected routes without login
- [ ] Logout functionality

**Fleet Management:**
- [ ] Add new truck
- [ ] View all trucks on dashboard
- [ ] Update truck status
- [ ] Delete truck
- [ ] View empty fleet state

**Tracking:**
- [ ] View trucks on map (requires Google Maps API key)
- [ ] View trucks in list view
- [ ] Test with multiple truck locations

**Scheduling:**
- [ ] Create new schedule
- [ ] View schedules
- [ ] Update schedule status

**Service Requests:**
- [ ] Submit service request
- [ ] View all requests
- [ ] Filter requests by truck

**Alerts:**
- [ ] Create alert
- [ ] Mark alert as read
- [ ] View unread count
- [ ] Filter by severity

## Security Considerations

- **Never commit API keys** - Use `.env` file
- **Hash passwords** - Already implemented with Werkzeug
- **Validate all input** - Check forms and API data
- **Use HTTPS in production** - Configure your deployment
- **Session security** - Don't expose session data
- **SQL injection** - MongoDB is NoSQL but still validate input
- **XSS protection** - Escape user input in templates

## Database Guidelines

### Schema Changes

If your contribution requires database changes:

1. Document the change in your PR
2. Provide example data
3. Consider backward compatibility
4. Update `models.py` functions
5. Update documentation

### Example Collections

```python
# Trucks
{
  "truck_id": "T001",
  "location": "40.7128,-74.0060",
  "speed": 65,
  "status": "Active"
}

# Alerts
{
  "alert_type": "maintenance",
  "truck_id": "T001",
  "message": "Oil change needed",
  "severity": "medium",
  "timestamp": datetime.now(),
  "read": False,
  "acknowledged": False
}
```

## Adding New Features

### New Routes
When adding new routes:
1. Add route decorator in `app.py`
2. Create corresponding template in `templates/`
3. Add navigation link in `base.html`
4. Update README.md with new route
5. Test thoroughly

### New Database Collections
When adding new collections:
1. Add collection in `db.py`
2. Create model functions in `models.py`
3. Update documentation
4. Consider relationships with existing data

### UI Components
When adding UI features:
1. Follow existing design patterns
2. Ensure responsive design
3. Add to `static/styles.css`
4. Test on multiple browsers
5. Ensure accessibility

## Performance Considerations

- **Database Queries**: Avoid N+1 queries, use projection
- **Template Rendering**: Keep templates lean
- **Static Files**: Minify CSS/JS for production
- **Caching**: Consider Flask-Caching for repeated queries
- **Pagination**: Implement for large datasets

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions
- Include code examples where helpful
- Update API route documentation
- Document environment variables

## Fleet Management Best Practices

When contributing features for fleet management:

- **Scalability**: Design for fleets of 100+ trucks
- **Real-time Updates**: Consider WebSocket for live data
- **Data Accuracy**: Validate location coordinates
- **User Experience**: Make common operations easy
- **Reporting**: Provide actionable insights
- **Alerts**: Clear, actionable notifications

## Questions?

Feel free to open an issue with the `question` label, or reach out to [@varun-dudipala](https://github.com/varun-dudipala).

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the project
- Show empathy towards other contributors
- Welcome newcomers to the project

Thank you for contributing to the Autonomous Trucks Fleet Management System!
