using System;
using System.Collections.Generic;
using System.Text;

namespace ReportCommon.ProcurementPlan
{
    public class ProcurementDesignAndProcess
    {
        public string Needs { get; set; }
        public string  Requirements { get; set; }
        public string Select { get; set; }
        public string Bids { get; set; }
        public string Evaluate { get; set; }
        public string Sow { get; set; }
        public ContractType contract { get; set; }
    }
}
