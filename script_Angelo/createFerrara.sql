USE [Hera]
GO

/****** Object:  Table [dbo].[Ferrara]    Script Date: 4/12/2021 5:09:35 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Ferrara](
	[data_ora] [datetime] NOT NULL,
	[livello] [float] NOT NULL,
	[portata] [float] NOT NULL,
	[cod_pozzo] [nvarchar](50) NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Ferrara]  WITH CHECK ADD  CONSTRAINT [FK_Ferrara_coord] FOREIGN KEY([cod_pozzo])
REFERENCES [dbo].[coord] ([cod_pozzo])
GO

ALTER TABLE [dbo].[Ferrara] CHECK CONSTRAINT [FK_Ferrara_coord]
GO


