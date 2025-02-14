using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using V2T.Models;
using V2T.Services;
using System.Threading.Tasks;

namespace V2T.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult Privacy()
        {
            return View();
        }
        public IActionResult AboutUs()
        {
            return View();
        }

        public IActionResult FAQ()
        {
            return View();
        }
        public IActionResult ServerCloud()
        {
            return View();
        }

        public IActionResult CloudAppDevelopment()
        {
            return View();
        }

        public IActionResult Cybersecurity()
        {
            return View();
        }



        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
