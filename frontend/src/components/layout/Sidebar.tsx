import React from 'react';
import { useState } from "react";
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  const linkStyle: React.CSSProperties = {
    padding: "10px 15px",
    borderRadius: "6px",
    textDecoration: "none",
    color: "white",
    fontFamily: "helvetica neue",
    fontSize: "14px",
    fontWeight: 500,
    display: "flex",
    alignItems: "center",
    whiteSpace: "nowrap",
    overflow: "hidden",
  };

  const activeStyle: React.CSSProperties = {
    background: "#2D2D2D",
  };

  return (
    <div
      style={{
        width: collapsed ? "70px" : "220px",
        background: "#2D2D2D",
        color: "white",
        padding: "20px 10px",
        display: "flex",
        flexDirection: "column",
        gap: "12px",
        height: "100vh",
        transition: "width 0.25s ease",
      }}
    >
      {/* Header + Collapse Button */}
      <div
        style={{
          display: "flex",
          justifyContent: collapsed ? "center" : "space-between",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        {!collapsed && (
          <h2 style={{ fontSize: "20px",fontFamily: "helvetica neue", margin: 0 }}>Dairy Analytics</h2>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          style={{
            background: "transparent",
            border: "1px solid #555",
            color: "white",
            borderRadius: "4px",
            cursor: "pointer",
            padding: "4px 8px",
           
          }}
        >
          {collapsed ? "→" : "←"}
        </button>
      </div>

      {/* Navigation Links */}
      <NavLink
        to="/dashboard"
        style={({ isActive }) =>
          isActive ? { ...linkStyle, ...activeStyle } : linkStyle
        }
        onMouseEnter={(e) =>
          (e.currentTarget.style.borderBottom = "2px solid #0B73B9")
        }
        onMouseLeave={(e) =>
          (e.currentTarget.style.borderBottom = "2px solid transparent")
        }
      >
        {!collapsed && "Dashboard"}
      </NavLink>

      <NavLink
        to="/production"
        style={({ isActive }) =>
          isActive ? { ...linkStyle, ...activeStyle } : linkStyle
        }
        onMouseEnter={(e) =>
          (e.currentTarget.style.borderBottom = "2px solid #0B73B9")
        }
        onMouseLeave={(e) =>
          (e.currentTarget.style.borderBottom = "2px solid transparent")
        }
      >
        {!collapsed && "Production"}
      </NavLink>

      <NavLink
        to="/Costs"
        style={({ isActive }) =>
          isActive ? { ...linkStyle, ...activeStyle } : linkStyle
        }
        onMouseEnter={(e) =>
          (e.currentTarget.style.borderBottom = "2px solid #0B73B9")
        }
        onMouseLeave={(e) =>
          (e.currentTarget.style.borderBottom = "2px solid transparent")
        }
      >
        {!collapsed && "Costs & Revenue"}
      </NavLink>

      <NavLink
        to="/marketdata"
        style={({ isActive }) =>
          isActive ? { ...linkStyle, ...activeStyle } : linkStyle
        }
        onMouseEnter={(e) =>
          (e.currentTarget.style.borderBottom = "2px solid #0B73B9")
        }
        onMouseLeave={(e) =>
          (e.currentTarget.style.borderBottom = "2px solid transparent")
        }
      >
        {!collapsed && "Market Trends"}
      </NavLink>

      <NavLink
        to="/dataupload"
        style={({ isActive }) =>
          isActive ? { ...linkStyle, ...activeStyle } : linkStyle
        }
        onMouseEnter={(e) =>
          (e.currentTarget.style.borderBottom = "2px solid #0B73B9")
        }
        onMouseLeave={(e) =>
          (e.currentTarget.style.borderBottom = "2px solid transparent")
        }
      >
        {!collapsed && "Data Upload"}
      </NavLink>
    </div>
  );
}
