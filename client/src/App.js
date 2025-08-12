import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Skeleton } from "./components/ui/skeleton";
import { ScrollArea } from "./components/ui/scroll-area";
import { Toaster } from "./components/ui/toaster";

// Simple API client
const apiClient = {
  async request(method, endpoint, data = null) {
    try {
      const options = {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
      };
      
      if (data) {
        options.body = JSON.stringify(data);
      }
      
      const response = await fetch(endpoint, options);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }
};

function SupplyChainDashboard() {
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [summary, setSummary] = useState(null);
  const [shipments, setShipments] = useState([]);
  const [trucks, setTrucks] = useState([]);
  const [distributionCenters, setDistributionCenters] = useState([]);
  const [stores, setStores] = useState([]);
  const [events, setEvents] = useState([]);
  const [weatherAlerts, setWeatherAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [
          summaryData,
          shipmentsData,
          trucksData,
          dcsData,
          storesData,
          eventsData,
          weatherData
        ] = await Promise.all([
          apiClient.request('GET', '/api/supply-chain/summary'),
          apiClient.request('GET', '/api/supply-chain/shipment'),
          apiClient.request('GET', '/api/supply-chain/truck'),
          apiClient.request('GET', '/api/supply-chain/distributioncenter'),
          apiClient.request('GET', '/api/supply-chain/store'),
          apiClient.request('GET', '/api/supply-chain/event'),
          apiClient.request('GET', '/api/supply-chain/weatheralert')
        ]);

        setSummary(summaryData);
        setShipments(shipmentsData);
        setTrucks(trucksData);
        setDistributionCenters(dcsData);
        setStores(storesData);
        setEvents(eventsData);
        setWeatherAlerts(weatherData);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getStatusBadgeVariant = (status) => {
    switch (status.toLowerCase()) {
      case "in transit":
      case "operational":
        return "default";
      case "delayed":
      case "maintenance":
        return "destructive";
      case "processing":
        return "secondary";
      default:
        return "outline";
    }
  };

  const getSeverityBadgeVariant = (severity) => {
    switch (severity.toLowerCase()) {
      case "high":
      case "critical":
        return "destructive";
      case "medium":
        return "secondary";
      case "low":
        return "outline";
      default:
        return "outline";
    }
  };

  const renderSummaryCards = () => {
    if (loading) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {[1, 2, 3, 4].map((i) => (
            <Card key={i}>
              <CardContent className="p-6">
                <Skeleton className="h-8 w-8 rounded-full mb-4" />
                <Skeleton className="h-4 w-20 mb-2" />
                <Skeleton className="h-8 w-12" />
              </CardContent>
            </Card>
          ))}
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-3 bg-blue-100 rounded-full">
                <i className="fas fa-warehouse text-blue-600 text-xl"></i>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Distribution Centers</p>
                <p className="text-2xl font-bold text-gray-900">{summary?.distribution_centers || 0}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-3 bg-green-100 rounded-full">
                <i className="fas fa-store text-green-600 text-xl"></i>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Stores</p>
                <p className="text-2xl font-bold text-gray-900">{summary?.stores || 0}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-3 bg-orange-100 rounded-full">
                <i className="fas fa-truck text-orange-600 text-xl"></i>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Trucks</p>
                <p className="text-2xl font-bold text-gray-900">{summary?.trucks || 0}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-3 bg-red-100 rounded-full">
                <i className="fas fa-exclamation-triangle text-red-600 text-xl"></i>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Issues</p>
                <p className="text-2xl font-bold text-gray-900">{events.filter(e => e.resolution_status === "Open").length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  };

  const renderMapView = () => (
    <Card className="h-96 mb-6">
      <CardHeader className="bg-gray-50">
        <div className="flex items-center justify-between">
          <CardTitle>🏭 Supply Chain Network Map</CardTitle>
          <div className="flex items-center space-x-4">
            <Select value={selectedFilter} onValueChange={setSelectedFilter}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Entities</SelectItem>
                <SelectItem value="issues">Issues & Delays</SelectItem>
                <SelectItem value="active_shipments">Active Shipments</SelectItem>
                <SelectItem value="weather_impacted">Weather Impacted</SelectItem>
              </SelectContent>
            </Select>
            <Button>
              <i className="fas fa-sync-alt mr-2"></i>Refresh
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-6 h-80 bg-gradient-to-br from-blue-50 to-indigo-100 relative">
        <div className="absolute inset-4 bg-white rounded-lg shadow-inner p-4 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <i className="fas fa-map-marked-alt text-4xl mb-4"></i>
            <p className="text-lg font-medium">Interactive Supply Chain Map</p>
            <p className="text-sm">Visualizing {distributionCenters.length} DCs, {stores.length} stores, and {trucks.length} trucks</p>
          </div>
        </div>
        
        {/* Legend */}
        <div className="absolute bottom-4 right-4 bg-white p-3 rounded-lg shadow-lg text-xs">
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-blue-600 rounded-full"></div>
              <span>Distribution Center</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-600 rounded-full"></div>
              <span>Store - Operational</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-orange-600 rounded-full"></div>
              <span>Issues/Maintenance</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const renderDataTables = () => (
    <Tabs defaultValue="shipments" className="space-y-6">
      <TabsList>
        <TabsTrigger value="shipments">Shipments</TabsTrigger>
        <TabsTrigger value="trucks">Fleet</TabsTrigger>
        <TabsTrigger value="events">Events</TabsTrigger>
        <TabsTrigger value="weather">Weather</TabsTrigger>
      </TabsList>
      
      <TabsContent value="shipments">
        <Card>
          <CardHeader>
            <CardTitle>Active Shipments</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-2">
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-12 w-full" />
                ))}
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Shipment ID</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Route</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Carrier</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ETA</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {shipments.map((shipment) => (
                      <tr key={shipment.shipment_id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{shipment.shipment_id}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <Badge variant={getStatusBadgeVariant(shipment.status)}>
                            {shipment.status}
                          </Badge>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{shipment.origin} → {shipment.destination}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{shipment.carrier}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{shipment.eta}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </TabsContent>

      <TabsContent value="trucks">
        <Card>
          <CardHeader>
            <CardTitle>Fleet Status</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-2">
                {[1, 2].map((i) => (
                  <Skeleton key={i} className="h-12 w-full" />
                ))}
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Truck ID</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Carrier</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Current Location</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Route</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {trucks.map((truck) => (
                      <tr key={truck.truck_id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{truck.truck_id}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{truck.carrier}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <Badge variant={getStatusBadgeVariant(truck.status)}>
                            {truck.status}
                          </Badge>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{truck.current_location}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{truck.route_id}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </TabsContent>

      <TabsContent value="events">
        <Card>
          <CardHeader>
            <CardTitle>Recent Events</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {events.map(event => (
                <div key={event.event_id} className={`p-4 rounded-lg border ${event.resolution_status.toLowerCase() === 'open' ? 'border-red-200 bg-red-50' : 'border-green-200 bg-green-50'}`}>
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-900">{event.event_type}</h4>
                      <p className="text-sm text-gray-600">Entity: {event.impacted_entity}</p>
                      {event.source && event.destination && (
                        <p className="text-sm text-gray-600">Route: {event.source} → {event.destination}</p>
                      )}
                      {event.description && (
                        <p className="text-sm text-gray-600">{event.description}</p>
                      )}
                      <p className="text-xs text-gray-500">{new Date(event.timestamp).toLocaleString()}</p>
                    </div>
                    <Badge variant={event.resolution_status === 'Open' ? 'destructive' : 'default'}>
                      {event.resolution_status}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      <TabsContent value="weather">
        <Card>
          <CardHeader>
            <CardTitle>Weather Alerts</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {weatherAlerts.map(alert => (
                <div key={alert.alert_id} className="p-4 rounded-lg border border-orange-200 bg-orange-50">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-semibold text-gray-900">{alert.alert_type}</h4>
                      <p className="text-sm text-gray-600">Region: {alert.region}</p>
                      <p className="text-xs text-gray-500">Date: {alert.date}</p>
                    </div>
                    <Badge variant={getSeverityBadgeVariant(alert.severity)}>
                      {alert.severity}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">🏭 Supply Chain Digital Twin</h1>
        <p className="text-gray-600">Ontology-Based Graph Model for Retail Supply Chain Management</p>
      </header>

      {renderSummaryCards()}
      {renderMapView()}
      {renderDataTables()}
    </div>
  );
}

function AIChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [inputMessage, setInputMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;
    
    const userMessage = {
      id: Date.now().toString(),
      role: "user",
      content: inputMessage,
      timestamp: new Date().toISOString(),
      userId: "demo-user"
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);
    
    try {
      console.log('Sending message to AI agent:', inputMessage);
      
      const response = await apiClient.request('POST', '/api/chat/messages', {
        role: "user",
        content: inputMessage,
        userId: "demo-user"
      });
      
      console.log('AI agent response:', response);
      
      // Fetch updated messages
      const updatedMessages = await apiClient.request('GET', '/api/chat/messages');
      console.log('Updated messages:', updatedMessages);
      setMessages(updatedMessages);
    } catch (error) {
      console.error('Failed to send message:', error);
      
      // Provide more specific error messages
      let errorMessage = "Sorry, I'm having trouble connecting right now. Please try again.";
      
      if (error.message.includes('Failed to fetch')) {
        errorMessage = "Cannot connect to the AI agent. Please check if the server is running.";
      } else if (error.message.includes('404')) {
        errorMessage = "AI agent endpoint not found. Please check the server configuration.";
      } else if (error.message.includes('500')) {
        errorMessage = "AI agent server error. Please try again later.";
      }
      
      // Add error message
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: errorMessage,
        timestamp: new Date().toISOString(),
        userId: "demo-user"
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatMessageContent = (content) => {
    return content.split('\n').map((line, index) => {
      if (line.startsWith('• ') || line.startsWith('- ')) {
        return <div key={index} className="ml-4">{line}</div>;
      }
      if (line.startsWith('**') && line.endsWith('**')) {
        const text = line.slice(2, -2);
        return <div key={index} className="font-semibold text-blue-600 mt-2 mb-1">{text}</div>;
      }
      if (line.includes('📦') || line.includes('🚛') || line.includes('🏭') || line.includes('🌦️') || line.includes('⚠️') || line.includes('📊')) {
        return <div key={index} className="font-medium text-gray-800 mt-2 mb-1">{line}</div>;
      }
      return line ? <div key={index}>{line}</div> : <div key={index} className="h-2"></div>;
    });
  };

  const quickPrompts = [
    "Show me current delays",
    "Weather impact summary", 
    "Fleet status overview",
    "Distribution center status"
  ];

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Chat Widget */}
      {isOpen && (
        <Card className="mb-4 w-96 h-96 shadow-2xl">
          {/* Chat Header */}
          <CardHeader className="p-4 bg-blue-600 text-white rounded-t-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                <div>
                  <h3 className="font-semibold">AI Assistant</h3>
                  <p className="text-xs opacity-90">Supply Chain Expert</p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsOpen(false)}
                className="text-white hover:text-gray-200 hover:bg-blue-700"
              >
                <i className="fas fa-times"></i>
              </Button>
            </div>
          </CardHeader>

          {/* Messages Container */}
          <ScrollArea className="h-64 p-4">
            <div className="space-y-4">
              {messages.length === 0 && (
                <div className="text-left">
                  <div className="inline-block bg-gray-100 p-3 rounded-lg text-sm max-w-xs">
                    <div className="space-y-1">
                      {formatMessageContent("Hi! I'm your Supply Chain AI Assistant. I can help you with shipment tracking, inventory queries, weather impacts, and operational insights. What would you like to know?")}
                    </div>
                  </div>
                  <div className="text-xs text-gray-500 mt-1">{new Date().toLocaleTimeString()}</div>
                </div>
              )}
              
              {messages.map((message) => (
                <div key={message.id} className={`${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                  <div className={`inline-block max-w-xs p-3 rounded-lg text-sm ${
                    message.role === 'user' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {message.role === 'assistant' ? (
                      <div className="space-y-1">
                        {formatMessageContent(message.content)}
                      </div>
                    ) : (
                      message.content
                    )}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              ))}
              
              {/* Typing Indicator */}
              {isLoading && (
                <div className="text-left">
                  <div className="inline-block bg-gray-100 p-3 rounded-lg">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          {/* Input Area */}
          <CardContent className="p-4 border-t">
            <div className="flex space-x-2">
              <Input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about shipments, delays, weather..."
                disabled={isLoading}
                className="flex-1"
              />
              <Button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isLoading}
                size="sm"
              >
                <i className="fas fa-paper-plane"></i>
              </Button>
            </div>
            <div className="mt-2 flex flex-wrap gap-2">
              {quickPrompts.map((prompt) => (
                <Button
                  key={prompt}
                  variant="outline"
                  size="sm"
                  onClick={() => setInputMessage(prompt)}
                  className="text-xs h-6 px-2"
                >
                  {prompt}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Chat Toggle Button */}
      <Button
        onClick={() => setIsOpen(!isOpen)}
        className="w-14 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 group"
        size="sm"
      >
        {isOpen ? (
          <i className="fas fa-times text-xl"></i>
        ) : (
          <>
            <i className="fas fa-robot text-xl group-hover:scale-110 transition-transform"></i>
            <div className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full text-xs flex items-center justify-center animate-pulse">
              AI
            </div>
          </>
        )}
      </Button>
    </div>
  );
}

function App() {
  return (
    <div className="min-h-screen">
      <SupplyChainDashboard />
      <AIChat />
      <Toaster />
    </div>
  );
}

export default App;
