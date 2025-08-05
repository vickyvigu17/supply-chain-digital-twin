# Supply Chain Digital Twin

🏭 **An Ontology-Based Graph Model for Retail Supply Chain Management**

Inspired by Palantir's digital twin approach, this application provides a comprehensive visualization and management system for retail supply chain operations, featuring companies like Kroger and Tractor Supply.

## 🌟 Features

### Interactive US Map Visualization
- **Distribution Centers**: 16 strategically located facilities across US regions
- **Retail Stores**: 200+ urban and rural locations with type indicators
- **Active Trucks**: 40 vehicles with real-time status and location tracking
- **Shipment Routes**: Visual representation of active and delayed shipments
- **Weather Impact**: Regional weather alerts affecting operations

### Comprehensive Supply Chain Entities

#### 🧱 Node Types
- **DistributionCenter**: Regional hubs with location and operational data
- **Store**: Retail locations with urban/rural classification
- **SKU**: 500+ products with categories and temperature zones
- **Truck**: Fleet vehicles with carrier info and route tracking
- **PurchaseOrder**: Order management with delivery windows
- **Shipment**: Cargo tracking with multiple transportation modes
- **InventorySnapshot**: Real-time inventory levels
- **Return**: Product returns with condition tracking
- **WeatherAlert**: Regional weather impact monitoring
- **Event**: Issue tracking and resolution management

#### 🔗 Relationships
- Distribution Centers supply Stores
- Trucks carry Shipments between locations
- Purchase Orders link to SKUs and Shipments
- Events track disruptions across entities
- Weather Alerts impact regional operations

### Interactive Filtering & Analytics
- **Issues & Delays**: Filter to show problematic entities
- **Active Shipments**: Track in-transit cargo
- **Weather Impacted**: View weather-affected regions
- **Real-time Data Tables**: Detailed entity information
- **Supply Chain Health Metrics**: KPIs and performance indicators
- **Regional Analysis**: Geographic distribution statistics

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 14+
- npm or yarn

### Installation & Build

1. **Clone and setup:**
```bash
git clone <your-repo>
cd supply-chain-digital-twin
```

2. **Build the application:**
```bash
chmod +x build.sh
./build.sh
```

3. **Start the server:**
```bash
chmod +x start.sh
./start.sh
```

4. **Access the application:**
Open your browser to `http://localhost:8000`

### Manual Setup

If you prefer manual setup:

1. **Backend Setup:**
```bash
python3 -m pip install -r requirements.txt --break-system-packages
```

2. **Frontend Setup:**
```bash
cd client
npm install
npm run build
cd ..
```

3. **Copy static files:**
```bash
cp -r client/build/* static/
```

4. **Start the server:**
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 API Endpoints

### Node Data
- `GET /api/nodes` - All supply chain entities
- `GET /api/nodes/{type}` - Specific entity type
  - Types: `distribution_centers`, `stores`, `trucks`, `purchase_orders`, `shipments`, `inventory`, `returns`, `weather_alerts`, `events`, `skus`

### Analytics
- `GET /api/summary` - Summary statistics
- `GET /api/relationships` - Entity relationships

### Examples
```bash
# Get all distribution centers
curl http://localhost:8000/api/nodes/distribution_centers

# Get supply chain summary
curl http://localhost:8000/api/summary

# Get all active events
curl http://localhost:8000/api/nodes/events
```

## 🎯 Use Cases

### Supply Chain Visibility
- **Real-time Tracking**: Monitor shipments, trucks, and inventory
- **Issue Management**: Track delays, shortages, and equipment failures
- **Weather Impact**: Assess weather-related disruptions
- **Performance Metrics**: Analyze delivery rates and operational efficiency

### Decision Support
- **Route Optimization**: Visualize truck routes and identify bottlenecks
- **Inventory Planning**: Monitor stock levels across locations
- **Risk Management**: Identify vulnerable supply chain segments
- **Resource Allocation**: Optimize distribution center capacity

### Business Intelligence
- **Regional Analysis**: Compare performance across geographic regions
- **Trend Analysis**: Track historical patterns and seasonal variations
- **Operational Insights**: Identify improvement opportunities
- **Compliance Monitoring**: Ensure regulatory requirements are met

## 🏗️ Architecture

### Backend (FastAPI)
- **Data Generation**: Realistic sample data for all entity types
- **RESTful API**: Clean endpoints for data access
- **Real-time Updates**: Dynamic data refresh capabilities
- **Scalable Design**: Modular structure for easy extension

### Frontend (React)
- **Interactive Map**: US map with clickable entities
- **Responsive Design**: Mobile and desktop friendly
- **Multi-view Interface**: Map, data tables, and analytics views
- **Real-time Filtering**: Dynamic content updates

### Data Model
- **Ontology-based**: Structured relationships between entities
- **Graph Structure**: Interconnected supply chain network
- **Temporal Data**: Time-based tracking and historical records
- **Extensible Schema**: Easy addition of new entity types

## 🔧 Configuration

### Environment Variables
```bash
REACT_APP_API_URL=http://localhost:8000  # Backend URL for frontend
```

### Data Customization
Modify `main.py` to adjust:
- Number of entities generated
- Geographic distribution
- Relationship patterns
- Business rules and constraints

## 🛠️ Development

### Adding New Entity Types
1. Define dataclass in `main.py`
2. Add to `generate_sample_data()`
3. Create API endpoint
4. Update frontend components

### Extending Relationships
1. Modify `get_relationships()` endpoint
2. Add visualization logic to `MapView.js`
3. Update filtering logic in `App.js`

### Custom Analytics
1. Add new API endpoints in `main.py`
2. Create analytics components in React
3. Update navigation and routing

## 📈 Sample Data

The application generates realistic sample data including:
- **16 Distribution Centers** across major US cities
- **200 Stores** with urban/rural distribution
- **500 SKUs** across multiple product categories
- **40 Trucks** with various carriers and statuses
- **60 Purchase Orders** with delivery windows
- **15 Active Shipments** with different modes
- **10 Weather Alerts** affecting operations
- **11 Events** tracking operational issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by Palantir's digital twin architecture
- Built for retail supply chain management
- Designed for companies like Kroger and Tractor Supply
- Uses real US geographic data for authentic visualization

---

**Built with ❤️ for modern supply chain management**