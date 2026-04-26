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
    fontSize: "16px",
    fontWeight: 500,
    display: "flex",
    alignItems: "center",
    whiteSpace: "nowrap",
    overflow: "hidden",
  };

  const activeStyle: React.CSSProperties = {
    background: "#3b3b55",
  };

  return (
    <div
      style={{
        width: collapsed ? "70px" : "220px",
        background: "#1e1e2f",
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
          <h2 style={{ fontSize: "20px", margin: 0 }}>Dairy Analytics</h2>
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
        to="/"
        style={({ isActive }) =>
          isActive ? { ...linkStyle, ...activeStyle } : linkStyle
        }
      >
        {!collapsed && "Dashboard"}
      </NavLink>

      <NavLink
        to="/herd"
        style={({ isActive }) =>
          isActive ? { ...linkStyle, ...activeStyle } : linkStyle
        }
      >
        {!collapsed && "Herd"}
      </NavLink>

      <NavLink
        to="/feed"
        style={({ isActive }) =>
          isActive ? { ...linkStyle, ...activeStyle } : linkStyle
        }
      >
        {!collapsed && "Feed"}
      </NavLink>

      <NavLink
        to="/forecast"
        style={({ isActive }) =>
          isActive ? { ...linkStyle, ...activeStyle } : linkStyle
        }
      >
        {!collapsed && "Forecast"}
      </NavLink>

      <NavLink
        to="/data"
        style={({ isActive }) =>
          isActive ? { ...linkStyle, ...activeStyle } : linkStyle
        }
      >
        {!collapsed && "Data Explorer"}
      </NavLink>
    </div>
  );
}
