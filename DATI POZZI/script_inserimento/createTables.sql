USE [Hera]
GO

/****** Object:  Table [dbo].[ForliCesena]    Script Date: 4/12/2021 5:10:11 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/*BOLOGNA*/
CREATE TABLE [dbo].[Bologna](
	[data_ora] [datetime] NOT NULL,
	[livello] [float] NOT NULL,
	[portata] [float] NOT NULL,
	[cod_pozzo] [nvarchar](50) NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Bologna]  WITH CHECK ADD  CONSTRAINT [FK_Bologna_coord] FOREIGN KEY([cod_pozzo])
REFERENCES [dbo].[coord] ([cod_pozzo])
GO

ALTER TABLE [dbo].[Bologna] CHECK CONSTRAINT [FK_Bologna_coord]
GO

/*Modena*/
CREATE TABLE [dbo].[Modena](
	[data_ora] [datetime] NOT NULL,
	[livello] [float] NOT NULL,
	[portata] [float] NOT NULL,
	[cod_pozzo] [nvarchar](50) NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Modena]  WITH CHECK ADD  CONSTRAINT [FK_Modena_coord] FOREIGN KEY([cod_pozzo])
REFERENCES [dbo].[coord] ([cod_pozzo])
GO

ALTER TABLE [dbo].[Modena] CHECK CONSTRAINT [FK_Modena_coord]
GO

/*Rimini*/
CREATE TABLE [dbo].[Rimini](
	[data_ora] [datetime] NOT NULL,
	[livello] [float] NOT NULL,
	[portata] [float] NOT NULL,
	[cod_pozzo] [nvarchar](50) NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Rimini]  WITH CHECK ADD  CONSTRAINT [FK_Rimini_coord] FOREIGN KEY([cod_pozzo])
REFERENCES [dbo].[coord] ([cod_pozzo])
GO

ALTER TABLE [dbo].[Rimini] CHECK CONSTRAINT [FK_Rimini_coord]
GO

/*Ravenna*/
CREATE TABLE [dbo].[Ravenna](
	[data_ora] [datetime] NOT NULL,
	[livello] [float] NOT NULL,
	[portata] [float] NOT NULL,
	[cod_pozzo] [nvarchar](50) NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Ravenna]  WITH CHECK ADD  CONSTRAINT [FK_Ravenna_coord] FOREIGN KEY([cod_pozzo])
REFERENCES [dbo].[coord] ([cod_pozzo])
GO

ALTER TABLE [dbo].[Ravenna] CHECK CONSTRAINT [FK_Ravenna_coord]
GO

/*ForliCesena*/
CREATE TABLE [dbo].[ForliCesena](
	[data_ora] [datetime] NOT NULL,
	[livello] [float] NOT NULL,
	[portata] [float] NOT NULL,
	[cod_pozzo] [nvarchar](50) NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[ForliCesena]  WITH CHECK ADD  CONSTRAINT [FK_ForliCesena_coord] FOREIGN KEY([cod_pozzo])
REFERENCES [dbo].[coord] ([cod_pozzo])
GO

ALTER TABLE [dbo].[ForliCesena] CHECK CONSTRAINT [FK_ForliCesena_coord]
GO


