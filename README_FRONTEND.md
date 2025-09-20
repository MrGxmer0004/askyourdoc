# AskYourDoc Frontend - React Application

A modern, professional React frontend for the AskYourDoc AI-powered health analysis system. Built with Vite, Tailwind CSS, and designed for optimal user experience.

## 🚀 Features

- **Modern React Architecture**: Built with React 18 and Vite for fast development
- **Professional Design**: Clean, clinical aesthetic with teal color scheme
- **Responsive Layout**: Mobile-first design that works on all devices
- **File Upload**: Drag-and-drop interface for PDF and image files
- **Real-time Analysis**: Live integration with FastAPI backend
- **Comprehensive Results**: Four-pillar analysis display with tabbed interface
- **Medical Safety**: Built-in disclaimers and professional consultation prompts

## 🛠️ Technology Stack

- **React 18**: Modern React with hooks and functional components
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful, customizable icons
- **Fetch API**: Native browser API for HTTP requests

## 📁 Project Structure

```
src/
├── components/
│   ├── Header.jsx          # Sticky navigation with glass effect
│   ├── Hero.jsx            # Landing section with features
│   ├── Analyzer.jsx        # File upload and analysis form
│   ├── ResultsDisplay.jsx  # Four-pillar results display
│   ├── Footer.jsx          # Professional footer
│   └── Spinner.jsx         # Loading animation component
├── App.jsx                 # Main application component
├── main.jsx               # Application entry point
└── index.css              # Global styles and Tailwind imports
```

## 🎨 Design System

### Color Palette
- **Primary Teal**: #007A7A (main brand color)
- **Light Gray**: #F7FAFC (backgrounds)
- **Dark Charcoal**: #1A202C (text)
- **Status Colors**: Green (normal), Orange (high/low), Red (critical)

### Typography
- **Headings**: Poppins (modern, professional)
- **Body Text**: Inter (highly readable)
- **Font Weights**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

### Components
- **Cards**: Rounded corners, soft shadows, hover effects
- **Buttons**: Gradient backgrounds, smooth transitions
- **Forms**: Clean inputs with focus states
- **Tables**: Responsive design with hover states

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Backend server running on http://localhost:8000

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

3. **Open in browser**
   ```
   http://localhost:3000
   ```

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## 🔧 Configuration

### Backend URL
The frontend is configured to connect to the backend at `http://localhost:8000`. To change this:

1. Open `src/components/Analyzer.jsx`
2. Update the `API_BASE_URL` constant:
   ```javascript
   const API_BASE_URL = 'https://your-backend-url.com';
   ```

### Styling Customization
- **Colors**: Edit `tailwind.config.js` to modify the color palette
- **Fonts**: Update font imports in `index.html`
- **Components**: Modify individual component files for specific styling

## 📱 Responsive Design

The application is fully responsive with breakpoints:
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px  
- **Desktop**: > 1024px

### Mobile Features
- Collapsible navigation menu
- Touch-friendly file upload
- Optimized table layouts
- Swipe-friendly tabs

## 🔌 API Integration

### Endpoints Used
- `POST /analyze/lab-report` - Main analysis endpoint
- `GET /health` - Health check (optional)

### Request Format
```javascript
const formData = new FormData();
formData.append('file', file);
formData.append('user_symptoms', userNotes);

fetch('/analyze/lab-report', {
  method: 'POST',
  body: formData
});
```

### Response Handling
The application expects a JSON response with the structure defined in the backend documentation.

## 🎯 User Experience Features

### File Upload
- **Drag & Drop**: Visual feedback during file drag
- **File Validation**: Type and size checking
- **Progress Indication**: Loading states during upload
- **Error Handling**: Clear error messages

### Results Display
- **Tabbed Interface**: Organized presentation of results
- **Status Badges**: Color-coded biomarker status
- **Risk Indicators**: Clear risk level visualization
- **Action Buttons**: Download and share functionality

### Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Screen Readers**: Proper ARIA labels
- **Color Contrast**: WCAG compliant colors
- **Focus Management**: Clear focus indicators

## 🧪 Testing

### Manual Testing Checklist
- [ ] File upload with PDF
- [ ] File upload with images
- [ ] Drag and drop functionality
- [ ] Form validation
- [ ] Error handling
- [ ] Results display
- [ ] Mobile responsiveness
- [ ] Tab navigation

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🚀 Deployment

### Vercel (Recommended)
1. Connect your GitHub repository to Vercel
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Deploy automatically on push

### Netlify
1. Build the project: `npm run build`
2. Upload the `dist` folder to Netlify
3. Configure redirects for SPA routing

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🔒 Security Considerations

- **File Upload**: Client-side validation (backend also validates)
- **XSS Protection**: React's built-in XSS protection
- **HTTPS**: Always use HTTPS in production
- **CORS**: Configured for localhost development

## 📊 Performance

### Optimization Features
- **Code Splitting**: Automatic with Vite
- **Tree Shaking**: Unused code elimination
- **Image Optimization**: Optimized asset loading
- **Lazy Loading**: Components loaded as needed

### Bundle Size
- **Development**: ~2MB (with dev tools)
- **Production**: ~200KB (gzipped)

## 🐛 Troubleshooting

### Common Issues

**Backend Connection Failed**
- Ensure backend is running on port 8000
- Check CORS configuration
- Verify API endpoint URLs

**File Upload Issues**
- Check file size limits (10MB)
- Verify supported file types
- Ensure proper FormData construction

**Styling Issues**
- Clear browser cache
- Restart development server
- Check Tailwind CSS compilation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the backend documentation
3. Check browser console for errors
4. Ensure all dependencies are installed

---

**Note**: This frontend is designed to work with the AskYourDoc FastAPI backend. Ensure the backend is running and properly configured before using the frontend application.
