# Tour Agent Planner

An AI-powered travel itinerary planning system that enables users to interact with Large Language Models (LLMs) through text or speech to craft personalized travel itineraries through turn-by-turn conversations.

---

## Getting Started

### Prerequisites

Before running the application, ensure you have the following installed on your system:

#### System Requirements

- **Node.js**: Version 20.0.0 or higher
- **Python**: Version 3.8 or higher
- **npm** or **yarn**: For managing frontend dependencies
- **pip**: For managing Python dependencies

#### API Keys (Required for LLM Integration)

You'll need API keys from one or more of the following providers:

- **OpenAI API Key**: For GPT models
- **Google Generative AI API Key**: For Gemini models

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/KohJunJie/tour-agent-planner.git
cd tour-agent-planner
```

#### 2. Backend Setup

Navigate to the backend directory and install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

**Backend Dependencies:**

- `fastapi` - Modern web framework for building APIs
- `uvicorn` - ASGI server for running FastAPI
- `python-socketio` - WebSocket support for real-time communication
- `langchain` - LLM orchestration framework
- `langchain-community` - Community integrations for LangChain
- `langchain-openai` - OpenAI integration for LangChain
- `google-generativeai` - Google Gemini AI integration
- `chromadb` - Vector database for agent memory
- `python-multipart` - File upload support
- `requests` - HTTP library for API calls

**Environment Configuration:**

Create a `.env` file in the `backend` directory with your API keys:

```bash
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

#### 3. Frontend Setup

Navigate to the frontend directory and install Node.js dependencies:

```bash
cd ../frontend
npm install
```

**Frontend Dependencies:**

- `react` (19.2.0) - UI library
- `react-dom` (19.2.0) - React DOM rendering
- `typescript` (~5.9.3) - Type safety
- `vite` (7.2.4) - Build tool and dev server
- `socket.io-client` (4.8.1) - WebSocket client
- `react-speech-recognition` (4.0.1) - Speech-to-text functionality
- `regenerator-runtime` (0.14.1) - Async/await support for speech recognition
- `lucide-react` (0.561.0) - Icon library

**Development Dependencies:**

- `@vitejs/plugin-react` - Vite React plugin
- `eslint` - Code linting
- `typescript-eslint` - TypeScript linting rules

### Running the Application

#### Start the Backend Server

From the `backend` directory:

```bash
python main.py
```

The backend server will start on `http://localhost:8000`

**Available Endpoints:**

- `GET /` - Root endpoint (health check)
- `GET /health` - Health status endpoint
- WebSocket connection on `ws://localhost:8000`

#### Start the Frontend Development Server

From the `frontend` directory:

```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

### Verify Installation

1. **Backend Health Check:**

   ```bash
   curl http://localhost:8000/health
   ```

   Expected response: `{"status": "ok"}`

2. **Frontend Access:**
   Open your browser and navigate to `http://localhost:5173`

3. **WebSocket Connection:**
   The frontend should automatically connect to the backend via Socket.IO. Check the browser console for "Connected to backend" message.

### Browser Compatibility

For speech recognition features, use a modern browser with Web Speech API support:

- **Chrome** (recommended)
- **Edge**
- **Safari** (limited support)
- **Firefox** (requires configuration)

### Troubleshooting

**Backend Issues:**

- Ensure Python 3.8+ is installed: `python --version`
- Verify all dependencies are installed: `pip list`
- Check that API keys are correctly set in `.env`
- Confirm port 8000 is not already in use

**Frontend Issues:**

- Ensure Node.js 20+ is installed: `node --version`
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check that port 5173 is not already in use
- Verify backend is running before starting frontend

**WebSocket Connection Issues:**

- Ensure CORS is properly configured in backend
- Check browser console for connection errors
- Verify firewall is not blocking WebSocket connections

---

## System Architecture Overview

### High-Level Architecture

The system follows a **client-server architecture** with real-time bidirectional communication capabilities:

```
┌────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                         │
│  ┌────────────────────────────────────────────────────────┐    │
│  │   React + TypeScript (Vite)                            │    │
│  │   • Chat Interface                                     │    │
│  │   • Speech Recognition (react-speech-recognition)      │    │
│  │   • Real-time Communication (Socket.IO Client)         │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────┘
                              │
                              │ WebSocket / HTTP
                              │
┌───────────────────────────────────────────────────────────────┐
│                        Backend Layer                          │
│  ┌────────────────────────────────────────────────────────┐   │
│  │   FastAPI + Socket.IO Server                           │   │
│  │   • WebSocket Event Handlers                           │   │
│  │   • REST API Endpoints                                 │   │
│  │   • CORS Middleware                                    │   │
│  └────────────────────────────────────────────────────────┘   │
│                             │                                 │
│  ┌─────────────────────┬────┴────┬──────────────────────┐     │
│  │                     │         │                      │     │
│  │  Speech-to-Text     │  Agent  │   Vector Store       │     │
│  │  Module             │  System │   (ChromaDB)         │     │
│  │                     │         │                      │     │
│  │  • Audio Stream     │ Manager │   • Agent Memory     │     │
│  │    Processing       │ Flights │   • Conversation     │     │
│  │  • Transcription    │ Hotels  │     History          │     │
│  │    Interface        │         │   • Embeddings       │     │
│  └─────────────────────┴─────────┴──────────────────────┘     │
└───────────────────────────────────────────────────────────────┘
                              │
                              │ API Calls
                              │
┌────────────────────────────────────────────────────────────────┐
│                      External Services                         │
│  • LLM Providers (OpenAI, Google Generative AI)                │
│  • Speech-to-Text Services                                     │
│  • Travel APIs (Flights, Hotels, etc.)                         │
└────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### Frontend (React + TypeScript + Vite)

**Technology Stack:**

- **Framework:** React 19.2.0 with TypeScript
- **Build Tool:** Vite 7.2.4
- **Real-time Communication:** Socket.IO Client 4.8.1
- **Speech Recognition:** react-speech-recognition 4.0.1
- **UI Components:** lucide-react (icons)

**Key Features:**

- Interactive chat interface for natural language conversations
- Real-time bidirectional communication with backend
- Speech-to-text input capability for hands-free interaction
- Text-based chat input as alternative interaction method
- Responsive UI for travel itinerary planning

**Communication Patterns:**

- WebSocket connection via Socket.IO for real-time messaging
- Audio streaming for speech input
- Event-driven architecture for transcription and responses

---

### Backend (Python FastAPI + Socket.IO)

**Technology Stack:**

- **Framework:** FastAPI (async web framework)
- **Server:** Uvicorn (ASGI server)
- **WebSocket:** Python Socket.IO (async mode)
- **LLM Integration:** LangChain, LangChain-OpenAI, LangChain-Community
- **Vector Database:** ChromaDB
- **AI Models:** Google Generative AI, OpenAI

**Architecture Components:**

#### 1. **API Layer** (`backend/main.py`)

- RESTful endpoints for health checks and system status
- CORS middleware for cross-origin requests
- Socket.IO integration for WebSocket communication

#### 2. **Agent System** (`backend/src/agents/`)

- **Manager Agent:** Orchestrates the conversation flow and delegates to specialized agents
- **Flights Agent:** Handles flight search and booking inquiries
- **Hotels Agent:** Manages hotel recommendations and reservations
- Multi-agent architecture enables modular, domain-specific expertise

#### 3. **Speech Processing** (`backend/src/speech_to_txt/`)

- Audio stream processing interface
- Integration with speech-to-text services
- Real-time transcription of voice inputs

#### 4. **Vector Store** (`backend/agent_store.py`)

- **ChromaDB** persistent storage for agent memory
- Stores conversation history and context
- Enables semantic search over past interactions
- Maintains user preferences and learned behaviors

**Key Features:**

- Asynchronous request handling for high performance
- Real-time audio streaming and processing
- Context-aware conversations using vector embeddings
- LLM integration via LangChain for natural language understanding
- Persistent memory for personalized recommendations

---

## Data Flow

### Text-based Interaction Flow

```
User Types Message → Frontend Chat UI → Socket.IO Event
                                              ↓
                                     Backend Socket Handler
                                              ↓
                                       Manager Agent
                                              ↓
                          ┌───────────────────┴──────────────────┐
                          ↓                                       ↓
                  Flights Agent                            Hotels Agent
                          ↓                                       ↓
                      LLM Processing (OpenAI/Google)
                          ↓                                       ↓
                  Vector Store Query (ChromaDB)
                          ↓                                       ↓
                      Response Generated
                          ↓                                       ↓
                          └───────────────────┬──────────────────┘
                                              ↓
                                   Backend Socket Emit
                                              ↓
                                     Frontend Display
```

### Speech-based Interaction Flow

```
User Speaks → Browser Speech API → Audio Stream → Socket.IO Event
                                                        ↓
                                              Speech-to-Text Module
                                                        ↓
                                              Transcription Result
                                                        ↓
                                              [Same as Text Flow]
```

---

## Key Design Patterns

### 1. **Multi-Agent System**

- Specialized agents for different travel domains (flights, hotels)
- Manager agent coordinates and routes requests
- Enables scalability for adding new travel services (activities, restaurants, etc.)

### 2. **Event-Driven Architecture**

- Socket.IO for real-time bidirectional communication
- Asynchronous event handlers for non-blocking operations
- Decoupled frontend and backend communication

### 3. **Vector Memory Store**

- ChromaDB for semantic search and context retention
- Embeddings enable intelligent retrieval of relevant past conversations
- Persistent storage ensures continuity across sessions

### 4. **LLM Orchestration via LangChain**

- Abstraction layer for multiple LLM providers
- Chain-based processing for complex reasoning
- Community tools for extended functionality

---

## Technology Rationale

| Technology                   | Purpose                 | Rationale                                                         |
| ---------------------------- | ----------------------- | ----------------------------------------------------------------- |
| **React + TypeScript**       | Frontend framework      | Type safety, component reusability, modern UI development         |
| **Vite**                     | Build tool              | Fast development builds, HMR, optimized production bundles        |
| **FastAPI**                  | Backend framework       | Async support, automatic API docs, high performance               |
| **Socket.IO**                | Real-time communication | Bidirectional streaming, automatic reconnection, fallback support |
| **LangChain**                | LLM orchestration       | Provider abstraction, chain composition, rich ecosystem           |
| **ChromaDB**                 | Vector database         | Efficient semantic search, easy Python integration, local-first   |
| **react-speech-recognition** | Speech input            | Browser speech API wrapper, cross-browser compatibility           |

---

## Deployment Architecture

### Development Environment

```
Frontend (Port 5173)  ←→  Backend (Port 8000)
   Vite Dev Server          Uvicorn + FastAPI
```

### Production Considerations

- Frontend: Static build deployed to CDN or web server
- Backend: Containerized FastAPI application
- Vector Store: Persistent volume for ChromaDB data
- LLM APIs: Secure API key management
- WebSocket: Load balancing with sticky sessions

---

## Security Considerations

1. **CORS Configuration:** Currently set to allow all origins (development only)
2. **API Key Management:** Environment variables for LLM service credentials
3. **Data Privacy:** Conversation history stored locally in vector database
4. **Input Validation:** FastAPI request validation and sanitization
5. **WebSocket Authentication:** Session management for Socket.IO connections

---

## Scalability Features

- **Async Operations:** Non-blocking I/O throughout the stack
- **Modular Agents:** Easy to add new travel service agents
- **Vector Store:** Efficient similarity search scales with conversation history
- **LangChain Providers:** Swap LLM providers without code changes
- **Stateless Backend:** Horizontal scaling capability (with external session store)

---

## Future Enhancements

- [ ] Authentication and user management
- [ ] Multi-language support
- [ ] Integration with real travel booking APIs
- [ ] Advanced itinerary visualization
- [ ] Export itineraries (PDF, calendar events)
- [ ] Mobile application
- [ ] Voice output (Text-to-Speech)
- [ ] Multi-modal inputs (images, maps)

---
