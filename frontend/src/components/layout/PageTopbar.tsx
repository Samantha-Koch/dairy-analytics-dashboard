export default function PageTopbar({title, sections, onSelect}) {  
    return (
      <div style={{
        width: "100%",
        background: "#2b2b40",
        color: "white",
        padding: "20px 24px",
        borderBottom: "1px solid #ddd",
        boxSizing: "border-box",
      }}>
        <h1 style={{margin: 0, fontSize:"200%"}}>{title}</h1>
        <div
        style={{
          marginTop: "10px",
          display: "flex",
          gap: "20px",
          flexWrap: "wrap",
        }}
      >
        {sections.map((s) => (
          <button
            key={s.id}
            onClick={() => onSelect(s.id)}
            style={{
              background: "transparent",
              color: "white",
              border: "none",
              cursor: "pointer",
              fontSize: "80%",
              padding: "6px 0",
              borderBottom: "2px solid transparent",
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.borderBottom = "2px solid #4f8cff")
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.borderBottom = "2px solid transparent")
            }
          >
            {s.label}
          </button>
        ))}
        </div>
      </div>
    );
  }
  