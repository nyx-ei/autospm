using System;
using System.Collections.Generic;
using System.Text;

namespace ReportCommon.ProcurementPlan
{
    public class ProcurementDesignProcess
    {
        public string Need { get; set; }
        public string  Requirement { get; set; }
        public string Select { get; set; }
        public string Bid { get; set; }
        public string Evaluate { get; set; }
        public string Sow { get; set; }
        public ContractType contract { get; set; }
    }
}
