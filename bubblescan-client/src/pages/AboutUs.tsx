import "../styles/content.css";
function AboutUs() {
    return (
        <>
            <div className="Container">
                <h1 className="title">About Us</h1>
                <p className="subtitle">Bubble Scan</ p>
                <p className="description">
                    The chemistry department at SLU uses paper scantron (fill-in-the-bubble) sheets for exams.
                    To grade the exams, they physically take the papers to one of the two machines on campus capable of processing this data.
                    This process is time consuming and a bit risky - the machines are getting old and might break.
                    In general, they like using paper based fill-in-the-bubble exams, but are interested in digitizing the grading process through
                    software that presents them with detailed results, similar to the results they get from the physical scantron machines.
                    specific sheets used by the chemistry department are Scantron form number 95945. While not hugely expensive,
                    not having to order such sheets is a cost-saving. Most importantly, this software would replace the technology
                    that's becoming obsolete and simplify the grading process
                </p>
            </div>
        </>
    );
}

export default AboutUs;