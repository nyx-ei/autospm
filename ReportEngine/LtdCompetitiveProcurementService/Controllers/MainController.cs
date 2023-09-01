using Microsoft.AspNetCore.Mvc;
using ReportCommon;

namespace AutoSPM.WB.Report.LtdCompetitiveProcurementService.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class MainController : ControllerBase
    {
        private readonly ILogger<MainController> _logger;

        public MainController(ILogger<MainController> logger)
        {
            _logger = logger;
        }

        [HttpGet(Name = "GetProposals")]
        public IEnumerable<Proposal> Get()
        {
            return null;
        }
    }
}