export default function PageTopbar({title, sections, onSelect}) {  
    return (
      <div style={{
        width: "100%",
        background: "#000000",
        color: "white",
        padding: "20px 24px",
        borderBottom: "1px solid #ddd",
        boxSizing: "border-box",
      }}>
        <h1 style={{margin: 0,fontFamily: "helvetica neue", fontSize:"30pt"}}>{title}</h1>
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
              fontSize: "12pt",
              padding: "6px 0",
              borderBottom: "2px solid transparent",
              fontFamily: "helvetica neue",
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.borderBottom = "2px solid #0B73B9")
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
  