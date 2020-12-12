import torch 
from models import BaseVAE
from torch import nn
from torch.nn import functional as F
from .types_ import *

class BetaVAE(BaseVAE):
	num_iter = 0

	def __init__(self, in_channels: int, latent_dim: int, hidden_dims: List=None, beta: int=4, gamma: float=1000, max_capacity: int=25, Capacity_max_iter: int=1e5, loss_type: str='B', **kwargs) -> None:
		super(BetaVAE, self).__init__()
		
		self.latent_dim = latent_dim
		sef.beta = beta
		self.gamma = gamma
		self.loss_type = loss_type
		self.C_max = torch.Tensor([max_capacity])
		self.C_stop_iter = Capacity_max_iter

		# Build encoder
		modules = []
		if hidden_dims is None:
			hidden_dims = [32, 64, 128, 256, 512]

		for h_dim in hidden_dims:
			modules.append(nn.Sequential(
				nn.Conv2d(in_channels, out_channels=h_dim, kernel_size=3, stride=2, padding=1),
				nn.BatchNorm2d(h_dim),
				nn.LeakyReLU()
			))
			in_channels = h_dim

		self.encoder = nn.Sequential(*modules)
		self.fc_mu = nn.Linear(hidden_dims[-1]*4, latent_dim)
		self.fc_var = nn.Linear(hidden_dims[-1]*4, latent_dim)

		# Build decoder
		modules = []
		self.decoder_input = nn.Linear(latent_dim, hidden_dims[-1]*4)

		hidden_dims.reverse()

		for i in range(len(hidden_dims)-1):
			modules.append(nn.Sequential(
				nn.ConvTranspose2d(hidden_dims[i], hidden_dims[i+1], kernel_size=3, stride=2, padding=1, output_padding=1),
				nn.BatchNorm2d(hidden_dims[i+1],
				nn.LeakyReLU()
			))

		self.decoder = nn.Sequential(*modules)

		self.final_layer = nn.Sequential(
			nn.ConvTranspose2d(hidden_dims[-1], hidden_dims[-1], kernel_size=3, stride=2, padding=1, output_padding=1),
			nn.BatchNorm2d(hidden_dims[-1]
			nn.LeakyReLU()
			nn.Conv2d(hidden_dims[-1], out_channels=3, kernel_size=3, padding=1),
			nn.Tanh()
		)

	def encode(self, input: Tensor) -> List[Tensor]:
		result = self.encoder(input)
		result = torch.flatten(result, start_dim=1)

		mu = self.fc_mu(result)
		log_var = sellf.fc_var(result)

		return [mu, log_var]

	def decode(self, z: Tensor) -> Tensor:
		result = self.decoder_input(z)
		result = result.view(-1, 512, 2, 2)
		result = self.decoder(result)
		result = final_layer(result)
		return result

	def reparameterize(self, mu: Tensor, logvar: Tensor) -> Tensor:
		std = torch.exp(0.5 * logvar)
		eps = torch.randn_like(std)
		return eps * std + mu

	def forward(self, input: Tensor, **kwargs) -> Tensor:
		mu, log_var = self.encode(input)
		z = self.reparameterize(mu, log_var)
		return [self.decode(z), input, mu, log_var]

	def loss_function(self, *args, **kwargs) -> dict:
		self.num_iter += 1
		recons = args[0]
		input = args[1]
		mu = args[2]
		log_var = args[3]
		kld_weight = kwargs['M_N']

		recons_loss = F.mse_loss(recons, input)

		kld_loss = torch.mean(-0.5 * torch.sum(1 + log_var - mu ** 2 - log_var.exp(), dim=1), dim=0)

		if self.loss_type == 'H':
			loss = recons_loss _ self.beta * kld_weight * kld_loss
		elif self.loss_type == 'B':
			self.C_max = self.C_max.to(input.device)
			C = torch.clamp(self.C_max/self.C_stop_iter * self.num_iter, 0, self.C_max.data[0])
			loss = recons_loss + self.gamma * kld_weight * (kld_loss - C).abs()
		else:
			raise ValueError('Undefined loss type.')

		return {'loss': loss, 'Reconstruction_Loss': recons_loss, 'KLD': kld_loss}

	def sample(self, num_samples: int, current_device: int, **kwargs) -> Tensor:
		z = torch.randn(num_samples, self.latent_dim)
		z = z.to(current_device)

		samples = self.decode(z)
		return samples

	def generate(self, x: Tensor, **kwargs) -> Tensor:
		return self.forward(x)[0]
